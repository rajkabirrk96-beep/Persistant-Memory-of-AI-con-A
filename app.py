from flask import Flask, render_template, request, session, redirect, url_for
import csv, os, uuid, json, sqlite3, io
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'epistemic_alignment_conditionA_2024'

@app.after_request
def no_cache(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# ── ALL ROUNDS ────────────────────────────────────────────────────────────────
ALL_ROUNDS = {
    "Information Technology": [
        ( 1,"Nexora Systems",142.5,1.8,0.0035,"Dataflux Inc",87.2,3.7,0.0035),
        ( 2,"CloudPeak Corp",156.8,3.9,0.0035,"ByteWave Ltd",94.4,1.9,0.0035),
        ( 3,"QuantumBridge Inc",203.6,3.6,0.0035,"PixelStream Corp",118.9,1.4,0.0035),
        ( 4,"CipherCore Ltd",178.3,3.6,0.0035,"SoftNova Inc",132.6,1.6,0.0035),
        ( 5,"GridLogic Corp",145.2,1.0,0.0035,"VaultTech Ltd",159.4,3.6,0.0035),
        ( 6,"NeuralPath Inc",97.3,1.6,0.0035,"CodeSpire Corp",198.7,4.0,0.0035),
        ( 7,"DataSphere Ltd",122.5,1.9,0.0035,"SyncWave Inc",181.9,3.8,0.0035),
        ( 8,"ByteForge Corp",89.6,1.2,0.0035,"PulseNet Ltd",135.8,3.5,0.0035),
        ( 9,"CoreMatrix Inc",147.8,1.2,0.0035,"TechSpan Corp",201.3,3.4,0.0035),
        (10,"InfiniteLoop Ltd",162.1,1.2,0.0035,"NodeBridge Inc",184.2,3.8,0.0035),
        (11,"AlphaGrid Corp",99.8,3.9,0.0035,"SignalBase Ltd",125.3,1.6,0.0035),
        (12,"OmegaStack Inc",138.4,1.6,0.0035,"ProtoCore Corp",149.9,3.9,0.0035),
        (13,"ZenithTech Ltd",204.7,1.1,0.0035,"ApexFlow Inc",91.2,3.6,0.0035),
        (14,"VectorNet Corp",186.5,1.4,0.0035,"PrismData Ltd",102.1,3.6,0.0035),
        (15,"HelixSoft Inc",152.3,1.0,0.0035,"TerraLogic Corp",127.8,3.7,0.0035),
    ],
    "Health Care": [
        ( 1,"MediVance Corp",198.3,1.1,0.0035,"CurePoint Ltd",134.6,3.9,0.0035),
        ( 2,"BioNexus Inc",245.8,3.8,0.0035,"HealthBridge Corp",89.4,1.6,0.0035),
        ( 3,"PharmaPeak Ltd",312.6,1.9,0.0035,"WellPath Inc",167.9,3.8,0.0035),
        ( 4,"ClinixCore Corp",138.2,3.7,0.0035,"GenoBridge Ltd",249.3,1.5,0.0035),
        ( 5,"VitalStream Inc",92.4,1.0,0.0035,"MedixCore Corp",308.7,3.6,0.0035),
        ( 6,"PharmaLink Ltd",201.5,3.9,0.0035,"BioVault Inc",171.2,1.7,0.0035),
        ( 7,"NovaCure Corp",252.1,1.2,0.0035,"HealthSpan Ltd",141.4,3.8,0.0035),
        ( 8,"CellBridge Inc",315.4,4.0,0.0035,"GenePeak Corp",95.8,1.8,0.0035),
        ( 9,"MediCore Ltd",174.6,1.3,0.0035,"BioStream Inc",204.2,3.9,0.0035),
        (10,"LifePath Corp",144.3,3.6,0.0035,"PharmaVault Ltd",318.9,1.4,0.0035),
        (11,"CureStream Inc",98.6,1.1,0.0035,"MediBridge Corp",255.4,3.7,0.0035),
        (12,"BioLink Ltd",207.8,3.8,0.0035,"VitalCore Inc",322.1,1.6,0.0035),
        (13,"HealthNova Corp",177.3,1.0,0.0035,"ClinixStream Ltd",147.6,3.6,0.0035),
        (14,"GenoBridge Inc",258.7,3.9,0.0035,"MediVault Corp",211.4,1.7,0.0035),
        (15,"PharmaPulse Ltd",325.8,1.2,0.0035,"BioCore Inc",101.9,3.8,0.0035),
    ],
    "Energy": [
        ( 1,"SolarNexus Corp",156.4,3.7,0.0035,"PetroVance Ltd",203.2,1.5,0.0035),
        ( 2,"GreenPeak Inc",89.3,1.1,0.0035,"PowerBridge Corp",134.8,3.6,0.0035),
        ( 3,"OilStream Ltd",267.5,3.8,0.0035,"EnergyCore Inc",158.9,1.6,0.0035),
        ( 4,"FuelVault Corp",206.8,1.0,0.0035,"WindPath Ltd",92.4,3.7,0.0035),
        ( 5,"SolarBridge Inc",137.6,3.9,0.0035,"GasLink Corp",264.3,1.7,0.0035),
        ( 6,"TerraFuel Ltd",161.2,1.2,0.0035,"HydroNexus Inc",95.8,3.8,0.0035),
        ( 7,"PowerStream Corp",210.4,3.6,0.0035,"CoalVault Ltd",140.5,1.4,0.0035),
        ( 8,"NuclearBridge Inc",261.8,1.1,0.0035,"SolarCore Corp",213.7,3.9,0.0035),
        ( 9,"WindStream Ltd",163.9,3.7,0.0035,"GreenBridge Inc",143.2,1.5,0.0035),
        (10,"EcoFuel Corp",99.2,1.0,0.0035,"PetroLink Ltd",259.4,3.6,0.0035),
        (11,"HydroPath Inc",146.3,3.8,0.0035,"SolarVault Corp",167.1,1.6,0.0035),
        (12,"GasPeak Ltd",217.6,1.2,0.0035,"WindCore Inc",102.5,3.7,0.0035),
        (13,"BiofuelBridge Corp",257.2,3.9,0.0035,"PowerNexus Ltd",149.4,1.7,0.0035),
        (14,"TerraStream Inc",170.8,1.1,0.0035,"FuelCore Corp",221.3,3.8,0.0035),
        (15,"EnergyVault Ltd",105.9,3.6,0.0035,"GreenStream Inc",174.2,1.4,0.0035),
    ],
    "Financials": [
        ( 1,"CapitalNexus Corp",312.4,1.3,0.0035,"WealthBridge Ltd",187.6,3.9,0.0035),
        ( 2,"BankStream Inc",156.8,3.7,0.0035,"InvestCore Corp",234.5,1.5,0.0035),
        ( 3,"FinVault Ltd",289.3,1.0,0.0035,"TrustPeak Inc",315.7,3.8,0.0035),
        ( 4,"CreditBridge Corp",191.2,3.9,0.0035,"AssetStream Ltd",159.4,1.7,0.0035),
        ( 5,"WealthNexus Inc",238.8,1.2,0.0035,"EquityCore Corp",286.1,3.6,0.0035),
        ( 6,"MoneyPath Ltd",318.9,3.8,0.0035,"FundBridge Inc",242.3,1.6,0.0035),
        ( 7,"TrustStream Corp",162.6,1.1,0.0035,"BankVault Ltd",194.8,3.7,0.0035),
        ( 8,"InvestLink Inc",283.4,3.9,0.0035,"CapitalCore Corp",246.1,1.8,0.0035),
        ( 9,"AssetNexus Ltd",322.5,1.0,0.0035,"WealthStream Inc",165.3,3.8,0.0035),
        (10,"EquityBridge Corp",198.6,3.6,0.0035,"FinCore Ltd",281.2,1.4,0.0035),
        (11,"FundNexus Inc",249.8,1.2,0.0035,"CreditStream Corp",326.4,3.9,0.0035),
        (12,"MoneyCore Ltd",168.2,3.7,0.0035,"TrustLink Inc",279.3,1.5,0.0035),
        (13,"BankPath Corp",202.4,1.1,0.0035,"InvestVault Ltd",253.2,3.8,0.0035),
        (14,"CapitalStream Inc",277.5,3.9,0.0035,"WealthCore Corp",171.6,1.7,0.0035),
        (15,"FinBridge Ltd",330.2,1.0,0.0035,"AssetLink Inc",206.8,3.6,0.0035),
    ],
    "Consumer Discretionary": [
        ( 1,"RetailNexus Corp",234.5,1.1,0.0035,"ShopStream Ltd",156.8,3.8,0.0035),
        ( 2,"BrandCore Inc",189.3,3.9,0.0035,"MarketVault Corp",98.4,1.7,0.0035),
        ( 3,"StyleBridge Ltd",312.6,1.4,0.0035,"TrendLink Inc",237.2,3.6,0.0035),
        ( 4,"LuxuryStream Corp",160.4,3.8,0.0035,"FashionCore Ltd",192.8,1.6,0.0035),
        ( 5,"RetailVault Inc",101.3,1.0,0.0035,"BrandStream Corp",309.4,3.7,0.0035),
        ( 6,"ShopNexus Ltd",239.8,3.9,0.0035,"MarketCore Inc",104.6,1.8,0.0035),
        ( 7,"StyleStream Corp",196.2,1.2,0.0035,"TrendVault Ltd",163.9,3.8,0.0035),
        ( 8,"LuxuryCore Inc",306.8,3.6,0.0035,"FashionLink Corp",107.4,1.4,0.0035),
        ( 9,"RetailPath Ltd",242.5,1.1,0.0035,"BrandVault Inc",199.6,3.9,0.0035),
        (10,"ShopBridge Corp",167.3,3.7,0.0035,"MarketStream Ltd",304.2,1.5,0.0035),
        (11,"StyleNexus Inc",110.8,1.0,0.0035,"TrendCore Corp",245.3,3.8,0.0035),
        (12,"LuxuryLink Ltd",203.1,3.9,0.0035,"FashionVault Inc",301.8,1.7,0.0035),
        (13,"RetailCore Corp",170.6,1.2,0.0035,"BrandPath Ltd",114.2,3.6,0.0035),
        (14,"ShopStream Inc",299.5,3.8,0.0035,"MarketLink Corp",206.8,1.6,0.0035),
        (15,"StyleVault Ltd",248.4,1.1,0.0035,"TrendStream Inc",174.1,3.7,0.0035),
    ],
    "Consumer Staples": [
        ( 1,"GroceryNexus Corp",178.6,3.8,0.0035,"FoodStream Ltd",234.3,1.6,0.0035),
        ( 2,"HouseholdCore Inc",145.2,1.1,0.0035,"StapleVault Corp",189.7,3.9,0.0035),
        ( 3,"FoodBridge Ltd",180.4,3.7,0.0035,"GroceryCore Inc",147.8,1.5,0.0035),
        ( 4,"StapleStream Corp",237.1,1.0,0.0035,"HouseholdLink Ltd",192.4,3.8,0.0035),
        ( 5,"FoodNexus Inc",150.3,3.9,0.0035,"GroceryVault Corp",182.8,1.7,0.0035),
        ( 6,"StapleBridge Ltd",195.2,1.2,0.0035,"HouseholdCore Inc",184.9,3.6,0.0035),
        ( 7,"FoodVault Corp",239.8,3.8,0.0035,"GroceryLink Ltd",153.1,1.4,0.0035),
        ( 8,"StapleCore Inc",187.3,1.1,0.0035,"HouseholdStream Corp",198.0,3.9,0.0035),
        ( 9,"FoodPath Ltd",156.4,3.7,0.0035,"GroceryStream Inc",242.6,1.5,0.0035),
        (10,"StapleNexus Corp",201.2,1.0,0.0035,"HouseholdVault Ltd",190.1,3.8,0.0035),
        (11,"FoodCore Inc",192.6,3.9,0.0035,"GroceryPath Corp",159.2,1.7,0.0035),
        (12,"StapleStream Ltd",245.8,1.2,0.0035,"HouseholdNexus Inc",204.4,3.6,0.0035),
        (13,"FoodLink Corp",162.3,3.8,0.0035,"GroceryBridge Ltd",195.2,1.6,0.0035),
        (14,"StaplePath Inc",208.1,1.1,0.0035,"HouseholdCore Corp",248.9,3.7,0.0035),
        (15,"FoodStream Ltd",198.1,3.9,0.0035,"GroceryNova Inc",165.8,1.8,0.0035),
    ],
    "Industrials": [
        ( 1,"AeroNexus Corp",287.4,3.7,0.0035,"ManufactureCore Ltd",198.6,1.5,0.0035),
        ( 2,"TransportStream Inc",156.8,1.1,0.0035,"IndustryVault Corp",234.2,3.8,0.0035),
        ( 3,"BuildNexus Ltd",312.5,3.9,0.0035,"AeroBridge Corp",291.3,1.7,0.0035),
        ( 4,"ManufactureLink Inc",201.4,1.0,0.0035,"TransportCore Ltd",159.6,3.6,0.0035),
        ( 5,"IndustryStream Corp",237.8,3.8,0.0035,"BuildCore Inc",309.2,1.6,0.0035),
        ( 6,"AeroVault Ltd",294.8,1.2,0.0035,"ManufactureNexus Corp",241.3,3.9,0.0035),
        ( 7,"TransportBridge Inc",162.4,3.7,0.0035,"IndustryCore Ltd",204.8,1.5,0.0035),
        ( 8,"BuildStream Corp",306.8,1.1,0.0035,"AeroLink Inc",244.6,3.8,0.0035),
        ( 9,"ManufactureVault Ltd",298.2,3.9,0.0035,"TransportNexus Corp",165.3,1.7,0.0035),
        (10,"IndustryBridge Inc",208.2,1.0,0.0035,"BuildVault Ltd",304.5,3.6,0.0035),
        (11,"AeroStream Corp",247.8,3.8,0.0035,"ManufactureCore Inc",302.1,1.6,0.0035),
        (12,"TransportVault Ltd",168.2,1.2,0.0035,"IndustryLink Corp",211.6,3.7,0.0035),
        (13,"BuildBridge Inc",302.3,3.9,0.0035,"AeroCore Ltd",251.2,1.8,0.0035),
        (14,"ManufactureStream Corp",305.9,1.1,0.0035,"TransportLink Inc",171.5,3.8,0.0035),
        (15,"IndustryNexus Ltd",215.0,3.6,0.0035,"BuildStream Corp",300.1,1.4,0.0035),
    ],
    "Materials": [
        ( 1,"ChemNexus Corp",156.4,1.0,0.0035,"MiningCore Ltd",234.8,3.8,0.0035),
        ( 2,"PackageStream Inc",89.3,3.9,0.0035,"MaterialVault Corp",178.6,1.7,0.0035),
        ( 3,"ChemBridge Ltd",158.9,1.2,0.0035,"MiningLink Inc",92.1,3.6,0.0035),
        ( 4,"PackageCore Corp",237.6,3.8,0.0035,"MaterialStream Ltd",181.4,1.6,0.0035),
        ( 5,"ChemVault Inc",94.8,1.1,0.0035,"MiningVault Corp",161.4,3.7,0.0035),
        ( 6,"PackageNexus Ltd",184.2,3.9,0.0035,"MaterialCore Inc",163.8,1.8,0.0035),
        ( 7,"ChemStream Corp",240.4,1.0,0.0035,"MiningBridge Ltd",97.6,3.8,0.0035),
        ( 8,"PackageBridge Inc",166.2,3.6,0.0035,"MaterialLink Corp",187.0,1.4,0.0035),
        ( 9,"ChemCore Ltd",100.3,1.2,0.0035,"MiningStream Inc",243.2,3.9,0.0035),
        (10,"PackagePath Corp",189.8,3.7,0.0035,"MaterialBridge Ltd",168.9,1.5,0.0035),
        (11,"ChemLink Inc",171.6,1.1,0.0035,"MiningCore Corp",103.1,3.8,0.0035),
        (12,"PackageVault Ltd",246.3,3.9,0.0035,"MaterialNexus Inc",193.0,1.7,0.0035),
        (13,"ChemPath Corp",105.8,1.0,0.0035,"MiningLink Ltd",174.3,3.6,0.0035),
        (14,"PackageStream Inc",196.4,3.8,0.0035,"MaterialCore Corp",249.8,1.6,0.0035),
        (15,"ChemNova Ltd",177.2,1.2,0.0035,"MiningVault Inc",108.6,3.7,0.0035),
    ],
    "Real Estate": [
        ( 1,"PropNexus Corp",234.6,3.9,0.0035,"REITStream Ltd",312.8,1.7,0.0035),
        ( 2,"EstateCore Inc",178.3,1.1,0.0035,"PropertyVault Corp",156.4,3.8,0.0035),
        ( 3,"PropBridge Ltd",237.4,3.6,0.0035,"REITCore Inc",181.6,1.4,0.0035),
        ( 4,"EstateStream Corp",316.2,1.0,0.0035,"PropertyLink Ltd",159.3,3.7,0.0035),
        ( 5,"PropVault Inc",184.9,3.8,0.0035,"REITBridge Corp",240.2,1.6,0.0035),
        ( 6,"EstateLink Ltd",162.1,1.2,0.0035,"PropertyCore Inc",243.1,3.9,0.0035),
        ( 7,"PropStream Corp",319.8,3.7,0.0035,"REITVault Ltd",188.3,1.5,0.0035),
        ( 8,"EstateNexus Inc",246.2,1.1,0.0035,"PropertyStream Corp",165.0,3.8,0.0035),
        ( 9,"PropCore Ltd",191.6,3.9,0.0035,"REITLink Inc",323.4,1.7,0.0035),
        (10,"EstateBridge Corp",167.8,1.0,0.0035,"PropertyNexus Ltd",249.3,3.6,0.0035),
        (11,"PropLink Inc",252.4,3.8,0.0035,"REITCore Corp",195.0,1.6,0.0035),
        (12,"EstateVault Ltd",327.2,1.2,0.0035,"PropertyBridge Inc",170.6,3.7,0.0035),
        (13,"PropStream Corp",198.3,3.9,0.0035,"REITPath Ltd",255.6,1.8,0.0035),
        (14,"EstateCore Inc",173.4,1.1,0.0035,"PropertyVault Corp",331.4,3.8,0.0035),
        (15,"PropNova Ltd",258.9,3.6,0.0035,"REITStream Inc",201.8,1.4,0.0035),
    ],
    "Utilities": [
        ( 1,"PowerNexus Corp",134.6,1.0,0.0035,"UtilityStream Ltd",189.3,3.8,0.0035),
        ( 2,"ElectricCore Inc",98.4,3.9,0.0035,"GasVault Corp",156.8,1.7,0.0035),
        ( 3,"PowerBridge Ltd",136.8,1.2,0.0035,"UtilityCore Inc",100.9,3.6,0.0035),
        ( 4,"ElectricStream Corp",192.1,3.8,0.0035,"GasLink Ltd",159.4,1.6,0.0035),
        ( 5,"PowerVault Inc",103.4,1.1,0.0035,"UtilityBridge Corp",139.2,3.7,0.0035),
        ( 6,"ElectricLink Ltd",162.1,3.9,0.0035,"GasCore Inc",141.6,1.8,0.0035),
        ( 7,"PowerStream Corp",195.0,1.0,0.0035,"UtilityVault Ltd",105.9,3.8,0.0035),
        ( 8,"ElectricNexus Inc",144.1,3.6,0.0035,"GasStream Corp",164.8,1.4,0.0035),
        ( 9,"PowerCore Ltd",108.4,1.2,0.0035,"UtilityLink Inc",197.9,3.9,0.0035),
        (10,"ElectricVault Corp",167.6,3.7,0.0035,"GasNexus Ltd",146.8,1.5,0.0035),
        (11,"PowerLink Inc",149.5,1.1,0.0035,"UtilityCore Corp",110.9,3.8,0.0035),
        (12,"ElectricBridge Ltd",200.8,3.9,0.0035,"GasVault Inc",170.4,1.7,0.0035),
        (13,"PowerStream Corp",113.4,1.0,0.0035,"UtilityNexus Ltd",152.2,3.6,0.0035),
        (14,"ElectricPath Inc",173.2,3.8,0.0035,"GasBridge Corp",203.7,1.6,0.0035),
        (15,"PowerNova Ltd",155.0,1.2,0.0035,"UtilityStream Inc",115.9,3.7,0.0035),
    ],
    "Communication Services": [
        ( 1,"MediaNexus Corp",267.4,1.1,0.0035,"TelecomCore Ltd",198.6,3.8,0.0035),
        ( 2,"StreamVault Inc",134.8,3.9,0.0035,"CommBridge Corp",312.4,1.7,0.0035),
        ( 3,"MediaCore Ltd",270.2,1.0,0.0035,"TelecomStream Inc",137.6,3.6,0.0035),
        ( 4,"StreamLink Corp",201.4,3.8,0.0035,"CommVault Ltd",315.8,1.6,0.0035),
        ( 5,"MediaBridge Inc",140.5,1.2,0.0035,"TelecomNexus Corp",273.1,3.9,0.0035),
        ( 6,"StreamCore Ltd",319.2,3.7,0.0035,"CommStream Inc",276.0,1.5,0.0035),
        ( 7,"MediaVault Corp",204.3,1.1,0.0035,"TelecomLink Ltd",143.4,3.8,0.0035),
        ( 8,"StreamNexus Inc",278.9,3.9,0.0035,"CommCore Corp",322.6,1.7,0.0035),
        ( 9,"MediaLink Ltd",146.3,1.0,0.0035,"TelecomVault Inc",207.2,3.6,0.0035),
        (10,"StreamBridge Corp",326.0,3.8,0.0035,"CommNexus Ltd",281.8,1.6,0.0035),
        (11,"MediaStream Inc",284.7,1.2,0.0035,"TelecomCore Corp",149.2,3.7,0.0035),
        (12,"StreamVault Ltd",210.1,3.9,0.0035,"CommLink Inc",329.4,1.8,0.0035),
        (13,"MediaNova Corp",152.1,1.1,0.0035,"TelecomBridge Ltd",287.6,3.8,0.0035),
        (14,"StreamCore Inc",332.8,3.6,0.0035,"CommVault Corp",213.4,1.4,0.0035),
        (15,"MediaPath Ltd",290.5,1.0,0.0035,"TelecomStream Corp",155.0,3.9,0.0035),
    ],
}

SECTOR_KEY = {
    "Information Technology":"Information_Technology",
    "Health Care":"Health_Care","Energy":"Energy",
    "Financials":"Financials",
    "Consumer Discretionary":"Consumer_Discretionary",
    "Consumer Staples":"Consumer_Staples",
    "Industrials":"Industrials","Materials":"Materials",
    "Real Estate":"Real_Estate","Utilities":"Utilities",
    "Communication Services":"Communication_Services",
}

# ── CHART GENERATION — runs automatically on first startup ────────────────────
def generate_all_charts():
    """Generate all 330 PNG charts and save to static/charts/
    Only runs if charts do not already exist — safe to call multiple times"""
    chart_dir = os.path.join(os.path.dirname(__file__), 'static', 'charts')
    os.makedirs(chart_dir, exist_ok=True)

    # Check if already generated
    existing = len([f for f in os.listdir(chart_dir) if f.endswith('.png')])
    if existing >= 330:
        print(f"Charts already exist ({existing} files) — skipping generation")
        return

    print("Generating stock charts — this takes about 60 seconds...")
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np
        import random

        def smooth_waypoints(growth_pct, seed, n=8):
            random.seed(seed)
            pts = [0.0]
            for i in range(1, n-1):
                progress = i/(n-1)
                base = growth_pct * progress
                var = growth_pct * 0.5 * (random.random() - 0.25)
                val = max(-0.2, base + var)
                pts.append(round(val, 2))
            pts.append(round(growth_pct, 1))
            return pts

        def catmull_rom(pts, n_out=300):
            """Smooth curve using Catmull-Rom spline — no scipy needed"""
            import numpy as np
            if len(pts) < 4:
                x = np.linspace(0, 6, len(pts))
                xi = np.linspace(0, 6, n_out)
                return np.interp(xi, x, pts)
            result = []
            x_wp = np.linspace(0, 6, len(pts))
            # Add phantom points at start and end
            p = [pts[0]] + list(pts) + [pts[-1]]
            x_ext = [x_wp[0]-(x_wp[1]-x_wp[0])] + list(x_wp) + [x_wp[-1]+(x_wp[-1]-x_wp[-2])]
            x_out = np.linspace(0, 6, n_out)
            for xi in x_out:
                # Find segment
                seg = 1
                for k in range(1, len(x_ext)-2):
                    if x_ext[k] <= xi <= x_ext[k+1]:
                        seg = k; break
                t = (xi - x_ext[seg]) / (x_ext[seg+1] - x_ext[seg] + 1e-9)
                t = max(0, min(1, t))
                p0,p1,p2,p3 = p[seg-1],p[seg],p[seg+1],p[seg+2]
                # Catmull-Rom formula
                y = 0.5*((2*p1) +
                    (-p0+p2)*t +
                    (2*p0-5*p1+4*p2-p3)*t*t +
                    (-p0+3*p1-3*p2+p3)*t*t*t)
                result.append(y)
            return np.array(result)

        def make_chart(sec_key, rnd, growth_pct, color_hex, stock_label, seed):
            fname = f"{sec_key}_R{rnd:02d}_{stock_label}.png"
            fpath = os.path.join(chart_dir, fname)
            if os.path.exists(fpath):
                return

            wpts = smooth_waypoints(growth_pct, seed)
            y_sm = catmull_rom(wpts)

            x_sm = np.linspace(0, 6, len(y_sm))

            fig, ax = plt.subplots(figsize=(5.5, 2.6))
            fig.patch.set_facecolor('white')
            ax.set_facecolor('white')

            ax.fill_between(x_sm, y_sm, 0,
                where=(y_sm>=0), color=color_hex, alpha=0.13)
            ax.fill_between(x_sm, y_sm, 0,
                where=(y_sm<0), color='#ef4444', alpha=0.07)
            ax.plot(x_sm, y_sm, color=color_hex, linewidth=2.0, zorder=5)
            ax.scatter([0],[0], color=color_hex, s=25, zorder=6)
            ax.scatter([6],[growth_pct], color=color_hex, s=25, zorder=6)
            ax.axhline(y=0, color='#94A3B8', linewidth=1.0,
                       linestyle='--', alpha=0.7, zorder=2)

            ax.set_ylim(-1, 10)
            ax.set_yticks([0,2,4,6,8,10])
            ax.set_yticklabels(['0%','2%','4%','6%','8%','10%'],
                               fontsize=7.5, color='#94A3B8')
            ax.set_ylabel('Change (%)', fontsize=7.5,
                          color='#64748B', labelpad=3)
            ax.set_xlim(0, 6)
            ax.set_xticks([0.5,1.5,2.5,3.5,4.5,5.5])
            ax.set_xticklabels(['M1','M2','M3','M4','M5','M6'],
                               fontsize=7.5, color='#94A3B8')

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E2E8F0')
            ax.spines['bottom'].set_color('#E2E8F0')
            ax.tick_params(length=0)
            ax.grid(False)

            plt.tight_layout(pad=0.4)
            plt.savefig(fpath, dpi=110, bbox_inches='tight',
                        facecolor='white', edgecolor='none')
            plt.close()

        count = 0
        for sector, rows in ALL_ROUNDS.items():
            sk = SECTOR_KEY.get(sector, sector.replace(' ','_'))
            for row in rows:
                rnd = row[0]; ga = row[3]; gb = row[7]
                make_chart(sk, rnd, ga, '#0F6E56', 'A',
                           seed=rnd*1000+abs(hash(sector))%1000)
                make_chart(sk, rnd, gb, '#6B21A8', 'B',
                           seed=rnd*2000+abs(hash(sector))%1000)
                count += 2

        print(f"Chart generation complete — {count} charts created")
    except Exception as e:
        print(f"Chart generation error: {e}")

def get_chart_url(sector, rnd, stock_label):
    sk = SECTOR_KEY.get(sector, sector.replace(' ','_'))
    return f"/static/charts/{sk}_R{rnd:02d}_{stock_label}.png"

def get_phase(rnd):
    if rnd<=5: return 1
    if rnd<=10: return 2
    return 3

def build_ai_text(rnd,sa,sb,goal,risk,hold,rd):
    phase=get_phase(rnd)
    if phase==1:
        return (f"Based on your <strong>{goal}</strong> investment goal, "
                f"your <strong>{risk}</strong> risk preference, and your "
                f"<strong>{hold}</strong> hold duration — both "
                f"<strong>{sa}</strong> and <strong>{sb}</strong> "
                f"are suitable for your portfolio this round.")
    elif phase==2:
        allocs=[float(rd.get(f'R{r}_alloc',50)) for r in range(1,6)]
        confs=[float(rd.get(f'R{r}_conf',50)) for r in range(1,6)]
        avg_s=sum(allocs)/len(allocs) if allocs else 50
        avg_a=round(avg_s*10); avg_b=1000-avg_a
        avg_c=round(sum(confs)/len(confs),1) if confs else 50.0
        return (f"Based on your <strong>{goal}</strong> investment goal, "
                f"your <strong>{risk}</strong> risk preference, your "
                f"<strong>{hold}</strong> hold duration, and your recent "
                f"investment pattern — averaging <strong>${avg_a}</strong> "
                f"toward Stock A and <strong>${avg_b}</strong> toward Stock B "
                f"with <strong>{avg_c}%</strong> average confidence — both "
                f"<strong>{sa}</strong> and <strong>{sb}</strong> "
                f"are suitable for your portfolio this round.")
    else:
        allocs=[float(rd.get(f'R{r}_alloc',50)) for r in range(1,11)]
        confs=[float(rd.get(f'R{r}_conf',50)) for r in range(1,11)]
        acis=[abs(float(rd.get(f'R{r}_alloc',50))-50)*2/100 for r in range(1,11)]
        avg_s=sum(allocs)/len(allocs) if allocs else 50
        avg_a=round(avg_s*10); avg_b=1000-avg_a
        avg_c=round(sum(confs)/len(confs),1) if confs else 50.0
        avg_ci=round(sum(acis)/len(acis),2) if acis else 0.0
        return (f"Based on your <strong>{goal}</strong> investment goal, "
                f"your <strong>{risk}</strong> risk preference, your "
                f"<strong>{hold}</strong> hold duration, and your consistent "
                f"investment pattern across 10 rounds — averaging "
                f"<strong>${avg_a}</strong> toward Stock A and "
                f"<strong>${avg_b}</strong> toward Stock B with "
                f"<strong>{avg_c}%</strong> average confidence and a "
                f"concentration index of <strong>{avg_ci}</strong> — both "
                f"<strong>{sa}</strong> and <strong>{sb}</strong> "
                f"are suitable for your portfolio this round.")

DB_FILE="/data/responses_A.db"
CSV_FILE="/data/responses_A.csv"

ALL_FIELDS=(
    ["participant_id","condition","sector","hold_duration",
     "investment_goal","risk_tolerance","prolific_id",
     "started_at","completed_at"]+
    [f"R{r}_{f}" for r in range(1,16)
     for f in ["stock_a","stock_b","alloc","conf","aci","return",
               "return_a","return_b"]]+
    ["total_return","benchmark_return","portfolio_score",
     "mean_confidence","mean_accuracy","oci","mean_aci","correct_rounds"]+
    ["back_attempts","back_rounds"]+
    ["age","gender","education","experience",
     "robo_prior","manipulation_check","open_text"]
)
CSV_HEADERS=ALL_FIELDS

def init_db():
    os.makedirs('/data',exist_ok=True)
    conn=sqlite3.connect(DB_FILE)
    cols=', '.join([f'"{f}" TEXT' for f in ALL_FIELDS])
    conn.execute(f'CREATE TABLE IF NOT EXISTS responses ({cols})')
    conn.commit(); conn.close()

def save_response(data):
    try:
        init_db()
        conn=sqlite3.connect(DB_FILE)
        fields=', '.join([f'"{f}"' for f in ALL_FIELDS])
        ph=', '.join(['?' for _ in ALL_FIELDS])
        vals=[str(data.get(f,'')) for f in ALL_FIELDS]
        conn.execute(f'INSERT INTO responses ({fields}) VALUES ({ph})',vals)
        conn.commit(); conn.close()
    except Exception as e: print(f"DB error:{e}")
    try:
        os.makedirs('/data',exist_ok=True)
        wh=not os.path.exists(CSV_FILE)
        with open(CSV_FILE,'a',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,fieldnames=ALL_FIELDS,extrasaction='ignore')
            if wh: w.writeheader()
            w.writerow(data)
    except Exception as e: print(f"CSV error:{e}")

def get_all_responses():
    try:
        init_db()
        conn=sqlite3.connect(DB_FILE)
        conn.row_factory=sqlite3.Row
        rows=conn.execute('SELECT * FROM responses ORDER BY rowid DESC').fetchall()
        conn.close(); return [dict(r) for r in rows]
    except: return []

def calc_feedback(rd,start_r,end_r):
    allocs,confs,acis=[],[],[]
    rounds_detail=[]; chart_data=[]
    for r in range(start_r,end_r+1):
        alloc=float(rd.get(f'R{r}_alloc',50))
        conf=float(rd.get(f'R{r}_conf',50))
        aci=abs(alloc-50)*2/100
        alloc_a=round(alloc*10); alloc_b=1000-alloc_a
        allocs.append(alloc); confs.append(conf); acis.append(aci)
        rounds_detail.append({"round":r,"alloc_a":alloc_a,"alloc_b":alloc_b,
            "conf":round(conf,1),"aci":round(aci,2)})
        chart_data.append({"round":r,"alloc_a":alloc_a,"alloc_b":alloc_b,
            "conf":round(conf,1),"aci":round(aci,2)})
    avg_s=sum(allocs)/len(allocs) if allocs else 50
    return {"avg_a":round(avg_s*10),"avg_b":1000-round(avg_s*10),
        "avg_conf":round(sum(confs)/len(confs),1) if confs else 50.0,
        "avg_aci":round(sum(acis)/len(acis),2) if acis else 0.0,
        "rounds":rounds_detail,"chart_data":chart_data}

def calc_final(sector,rd):
    rows=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])
    total_return=benchmark_return=correct=0
    allocs,confs,acis=[],[],[]
    for row in rows:
        rnd=row[0]; alloc=float(rd.get(f'R{rnd}_alloc',50))
        conf=float(rd.get(f'R{rnd}_conf',50))
        ga=row[3]; gb=row[7]; ra=ga/100; rb=gb/100
        aa=alloc*10; ab=1000-aa
        actual=(aa*ra)+(ab*rb); bench=(500*ra)+(500*rb)
        total_return+=actual; benchmark_return+=bench
        aci=abs(alloc-50)*2/100
        allocs.append(alloc); confs.append(conf); acis.append(aci)
        if actual>=bench: correct+=1
    mc=sum(confs)/len(confs) if confs else 50
    ma=(correct/15)*100
    return {"total_return":round(total_return,2),
        "benchmark_return":round(benchmark_return,2),
        "portfolio_score":round(total_return-benchmark_return,2),
        "mean_confidence":round(mc,1),"mean_accuracy":round(ma,1),
        "oci":round(mc-ma,1),
        "mean_aci":round(sum(acis)/len(acis),3) if acis else 0,
        "correct_rounds":correct}

URL_ORDER=['/','/sector','/prestudy']+\
    [f'/round/{r}' for r in range(1,16)]+\
    [f'/round/{r}/confidence' for r in range(1,16)]+\
    [f'/trajectory/{r}' for r in range(1,16)]+\
    ['/feedback/1','/feedback/2','/final_results','/post_survey','/thankyou']

def _is_behind(cur,far):
    try:
        ci=next((i for i,u in enumerate(URL_ORDER) if cur==u or cur.startswith(u)),999)
        fi=next((i for i,u in enumerate(URL_ORDER) if far==u or far.startswith(u)),0)
        return ci<fi
    except: return False

@app.route('/')
def index():
    session.clear()
    session['participant_id']=str(uuid.uuid4())[:8]
    session['prolific_id']=request.args.get('PROLIFIC_PID','')
    session['condition']='A'
    session['started_at']=datetime.now().isoformat()
    session['rd']={}
    session['furthest_url']='/'
    session['back_attempts']=0
    session['back_rounds']=[]
    return render_template('welcome.html')

@app.route('/sector')
def sector_page():
    session['furthest_url']='/sector'
    return render_template('sector.html')

@app.route('/sector',methods=['POST'])
def sector_submit():
    session['sector']=request.form.get('sector_choice','Information Technology')
    return redirect(url_for('prestudy'))

@app.route('/prestudy')
def prestudy():
    session['furthest_url']='/prestudy'
    return render_template('prestudy.html')

@app.route('/prestudy',methods=['POST'])
def prestudy_submit():
    session['hold_duration']=request.form.get('hold_duration','')
    session['investment_goal']=request.form.get('investment_goal','')
    session['risk_tolerance']=request.form.get('risk_tolerance','')
    return redirect(url_for('round_page',rnd=1))

@app.route('/round/<int:rnd>')
def round_page(rnd):
    if rnd<1 or rnd>15: return redirect(url_for('final_results'))
    furthest=session.get('furthest_url','/')
    current=f'/round/{rnd}'
    if _is_behind(current,furthest):
        # Track back attempt — force session modification
        attempts = session.get('back_attempts', 0) + 1
        rounds = session.get('back_rounds', [])
        rounds = list(rounds)  # make a new list — forces Flask to detect change
        rounds.append(f'R{rnd}')
        session['back_attempts'] = attempts
        session['back_rounds'] = rounds
        session.modified = True  # force Flask to save session
        return redirect(furthest)
    session['furthest_url']=current
    sector=session.get('sector','Information Technology')
    row=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    rnd_num,sa,pa,ga,va,sb,pb,gb,vb=row
    rd=session.get('rd',{})
    ai_text=build_ai_text(rnd,sa,sb,
        session.get('investment_goal',''),
        session.get('risk_tolerance',''),
        session.get('hold_duration',''),rd)
    phase=get_phase(rnd)
    return render_template('round.html',
        rnd=rnd,sa=sa,sb=sb,pa=pa,pb=pb,
        ai_text=ai_text,phase=phase,
        total_rounds=15,sector=sector)

@app.route('/round/<int:rnd>/submit',methods=['POST'])
def round_submit(rnd):
    sector=session.get('sector','Information Technology')
    alloc_a=float(request.form.get('alloc_a',500))
    alloc_pct=alloc_a/10
    row=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    rd=session.get('rd',{})
    rd[f'R{rnd}_stock_a']=row[1]; rd[f'R{rnd}_stock_b']=row[5]
    rd[f'R{rnd}_alloc']=alloc_pct
    rd[f'R{rnd}_return_a']=row[3]
    rd[f'R{rnd}_return_b']=row[7]
    session['rd']=rd
    session['furthest_url']=f'/round/{rnd}/confidence'
    return redirect(url_for('confidence_page',rnd=rnd))

@app.route('/round/<int:rnd>/confidence')
def confidence_page(rnd):
    furthest=session.get('furthest_url','/')
    current=f'/round/{rnd}/confidence'
    if _is_behind(current,furthest): return redirect(furthest)
    session['furthest_url']=current
    sector=session.get('sector','Information Technology')
    row=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    rnd_num,sa,pa,ga,va,sb,pb,gb,vb=row
    rd=session.get('rd',{})
    alloc_pct=rd.get(f'R{rnd}_alloc',50)
    alloc_a=round(alloc_pct*10); alloc_b=1000-alloc_a
    ai_text=build_ai_text(rnd,sa,sb,
        session.get('investment_goal',''),
        session.get('risk_tolerance',''),
        session.get('hold_duration',''),rd)
    return render_template('confidence.html',
        rnd=rnd,sa=sa,sb=sb,
        alloc_a=alloc_a,alloc_b=alloc_b,
        ai_text=ai_text,total_rounds=15,sector=sector)

@app.route('/round/<int:rnd>/confidence/submit',methods=['POST'])
def confidence_submit(rnd):
    sector=session.get('sector','Information Technology')
    conf=float(request.form.get('confidence',0))
    row=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    rd=session.get('rd',{})
    alloc_pct=rd.get(f'R{rnd}_alloc',50)
    aci=abs(alloc_pct-50)*2/100
    ga=row[3]; gb=row[7]; ra=ga/100; rb=gb/100
    aa=alloc_pct*10; ab=1000-aa
    actual=(aa*ra)+(ab*rb)
    rd[f'R{rnd}_conf']=conf
    rd[f'R{rnd}_aci']=round(aci,3)
    rd[f'R{rnd}_return']=round(actual,2)
    session['rd']=rd
    session['furthest_url']=f'/trajectory/{rnd}'
    return redirect(url_for('trajectory',rnd=rnd))

@app.route('/trajectory/<int:rnd>')
def trajectory(rnd):
    furthest=session.get('furthest_url','/')
    current=f'/trajectory/{rnd}'
    if _is_behind(current,furthest): return redirect(furthest)
    session['furthest_url']=current
    sector=session.get('sector','Information Technology')
    row=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])[rnd-1]
    rnd_num,sa,pa,ga,va,sb,pb,gb,vb=row
    chart_a=get_chart_url(sector,rnd,'A')
    chart_b=get_chart_url(sector,rnd,'B')
    if rnd==5:    next_url=url_for('feedback',phase=1)
    elif rnd==10: next_url=url_for('feedback',phase=2)
    elif rnd==15: next_url=url_for('final_results')
    else:         next_url=url_for('round_page',rnd=rnd+1)
    return render_template('trajectory.html',
        rnd=rnd,sa=sa,sb=sb,
        chart_a=chart_a,chart_b=chart_b,
        next_url=next_url,sector=sector)

@app.route('/feedback/<int:phase>')
def feedback(phase):
    furthest=session.get('furthest_url','/')
    current=f'/feedback/{phase}'
    if _is_behind(current,furthest): return redirect(furthest)
    session['furthest_url']=current
    sector=session.get('sector','Information Technology')
    rd=session.get('rd',{})
    start_r=1 if phase==1 else 6
    end_r=5 if phase==1 else 10
    summary=calc_feedback(rd,start_r,end_r)
    rows=ALL_ROUNDS.get(sector,ALL_ROUNDS["Information Technology"])
    feedback_charts=[]
    for r in range(start_r,end_r+1):
        row=rows[r-1]
        feedback_charts.append({
            "round":r,"sa":row[1],"sb":row[5],
            "chart_a":get_chart_url(sector,r,'A'),
            "chart_b":get_chart_url(sector,r,'B'),
        })
    return render_template('feedback.html',
        phase=phase,summary=summary,
        start_r=start_r,end_r=end_r,
        next_round=6 if phase==1 else 11,
        sector=sector,
        goal=session.get('investment_goal',''),
        risk=session.get('risk_tolerance',''),
        hold=session.get('hold_duration',''),
        feedback_charts=feedback_charts)

@app.route('/final_results')
def final_results():
    session['furthest_url']='/final_results'
    sector=session.get('sector','Information Technology')
    rd=session.get('rd',{})
    results=calc_final(sector,rd)
    session['final_results']=results
    return render_template('final_results.html',results=results)

@app.route('/post_survey',methods=['GET','POST'])
def post_survey():
    if request.method=='POST':
        sector=session.get('sector','Information Technology')
        rd=session.get('rd',{})
        results=session.get('final_results',calc_final(sector,rd))
        back_rounds = session.get('back_rounds', [])
        back_rounds_str = ','.join(str(r) for r in back_rounds) if back_rounds else ''
        back_attempts = int(session.get('back_attempts', 0))
        row={
            'participant_id':session.get('participant_id'),
            'condition':'A','sector':sector,
            'hold_duration':session.get('hold_duration'),
            'investment_goal':session.get('investment_goal'),
            'risk_tolerance':session.get('risk_tolerance'),
            'prolific_id':session.get('prolific_id'),
            'started_at':session.get('started_at'),
            'completed_at':datetime.now().isoformat(),
            **{k:v for k,v in rd.items()},**results,
            'back_attempts': back_attempts,
            'back_rounds':   back_rounds_str,
            'age':request.form.get('age'),
            'gender':request.form.get('gender'),
            'education':request.form.get('education'),
            'experience':request.form.get('experience'),
            'robo_prior':request.form.get('robo_prior'),
            'manipulation_check':request.form.get('manipulation_check'),
            'open_text':request.form.get('open_text'),
        }
        save_response(row)
        return redirect(url_for('thankyou',pid=session.get('prolific_id','')))
    session['furthest_url']='/post_survey'
    return render_template('post_survey.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html',pid=request.args.get('pid',''))

@app.route('/admin')
def admin():
    pw=request.args.get('pw','')
    if pw!='raj_admin_2024': return render_template('admin_login.html')
    rows=get_all_responses(); total=len(rows); responses=rows[:20]
    ocis=[]; cond_a=0
    for r in rows:
        try: ocis.append(float(r.get('oci',0)))
        except: pass
        if r.get('condition')=='A': cond_a+=1
    avg_oci=round(sum(ocis)/len(ocis),1) if ocis else 0
    return render_template('admin.html',total=total,responses=responses,
        avg_oci=avg_oci,cond_a=cond_a,cond_b=0)

@app.route('/data')
def download_data():
    pw=request.args.get('pw','')
    if pw!='raj_data_conditionA_2024': return "Access denied",403
    rows=get_all_responses()
    if not rows: return "No data yet",404
    output=io.StringIO()
    writer=csv.DictWriter(output,fieldnames=ALL_FIELDS,extrasaction='ignore')
    writer.writeheader(); writer.writerows(rows)
    return output.getvalue(),200,{'Content-Type':'text/csv',
        'Content-Disposition':'attachment; filename=responses_A.csv'}

@app.route('/ping')
def ping(): return 'alive',200

@app.route('/log_back', methods=['POST'])
def log_back():
    try:
        data = request.get_json()
        pid  = session.get('participant_id', 'unknown')
        url  = data.get('url', '') if data else ''
        ts   = datetime.now().isoformat()
        session['back_attempts'] = session.get('back_attempts', 0) + 1
        rounds = list(session.get('back_rounds', []))
        rounds.append(f"R_at_{ts[:19]}")
        session['back_rounds'] = rounds
        session.modified = True
        try:
            os.makedirs('/data', exist_ok=True)
            log_file = '/data/back_log.csv'
            wh = not os.path.exists(log_file)
            with open(log_file,'a',newline='',encoding='utf-8') as f:
                w = csv.writer(f)
                if wh:
                    w.writerow(['timestamp','participant_id',
                                'page_url','total_attempts'])
                w.writerow([ts, pid, url,
                            session.get('back_attempts',1)])
        except: pass
        return {'status':'logged'}, 200
    except:
        return {'status':'error'}, 200

@app.route('/backlog')
def download_backlog():
    pw = request.args.get('pw','')
    if pw != 'raj_data_conditionA_2024':
        return "Access denied", 403
    log_file = '/data/back_log.csv'
    if not os.path.exists(log_file):
        return "No back attempts recorded", 404
    with open(log_file,'r',encoding='utf-8') as f:
        content = f.read()
    return content, 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=back_log.csv'
    }

# Generate charts when app starts
generate_all_charts()

if __name__=='__main__':
    init_db()
    app.run(debug=True,port=5000)
