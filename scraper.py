import yfinance as yf
import json
import time
import os

def scrap_final_verified():
    # 필수 리스트 (BULZ, BERZ, FNGO, FNGS 포함)
    user_essential_list = [
        "BULZ", "BERZ", "FNGO", "FNGS", "TQQQ", "QLD", "SSO", "UPRO", "SQQQ", "AGQ", 
        "USD", "SH", "UGL", "SCO", "PSQ", "ROM", "UDOW", "UYG", "UCO", "SDS", "SPXU", 
        "DDM", "BOIL", "BITU", "QID", "URTY", "UVXY", "TBT", "UWM", "ETHT", "SBIT", 
        "SVXY", "SDOW", "KOLD", "BITI", "RWM", "CRCA", "ZSL", "MVV", "DOG", "SJB", 
        "GLL", "TBF", "DIG", "SRTY", "ETHD", "BIB", "RXL", "UBT", "TWM", "URE", 
        "DXD", "EUO", "YCL", "UYM", "URSP", "EET", "YCS", "UXI", "UMDD", "EFO", 
        "QQUP", "EFZ", "UPW", "UJB", "SAA", "SLON", "TTT", "SEF", "SKF", "SSG", 
        "DUG", "TBX", "SRS", "SETH", "UST", "EPV", "EEV", "EZJ", "EUM", "UGE", 
        "UPV", "REK", "UCC", "PST", "XPP", "NVDB", "SCC", "LTL", "EWV", "FXP", 
        "SIJ", "ULE", "REW", "SZK", "QQXL", "SDP", "YXI", "UBR", "SBB", "PLTA", 
        "RXD", "MYY", "UCYB", "SMN", "BZQ", "BIS", "COIA", "SMDD", "SDD", "EFU", 
        "QQDN", "SKYU", "MZZ", "TSLI", "SOXL", "SPXL", "TSLL", "TECL", "TMF", 
        "FAS", "SOXS", "TNA", "KORU", "NUGT", "MUU", "GGLL", "YINN", "MSFU", 
        "JNUG", "NVDU", "NAIL", "DPST", "LABU", "DFEN", "SPXS", "PLTU", "TSMX", 
        "METU", "AMZU", "TZA", "GUSH", "SPDN", "ERX", "CWEB", "SPUU", "TMV", 
        "EDC", "AVL", "NFXL", "AAPU", "BRZU", "FAZ", "CURE", "YANG", "FNGG", 
        "CHAU", "DRIP", "LABD", "WEBL", "TECS", "QQQU", "TSLS", "DUST", "MIDU", 
        "HIBL", "EURL", "INDL", "URAA", "DRN", "DUSL", "UTSL", "ERY", "AMUU", 
        "BRKU", "PLTD", "TYD", "JDST", "MUD", "DRV", "RETL", "UBOT", "QQQD", 
        "EDZ", "MEXX", "HIBS", "ORCU", "NVDD", "AAPD", "AIBU", "LINT", "WANT", 
        "ORCS", "TPOR", "AMDD", "GGLS", "WEBS", "ELIL", "PILL", "AMZD", "LMTL", 
        "TYO", "METD", "AVS", "SHPU", "MRVU", "MSFD", "LMBO", "NFXS", "AIBD", 
        "TEXU", "ASMU", "TSXU", "HODU", "CSCL", "QCMU", "TTXD", "TBXU", "QCMD", 
        "SHPD", "BABU", "CONX", "TTXU", "ELIS", "SOFA", "TSMZ", "FRDU", "FRDD", 
        "CSCS", "REKT", "TSXD", "LMTS", "BRKD", "ADBU", "BOED", "BOEU", "PALD", 
        "PALU", "PYPU", "TXNU", "UNHU", "XOMX", "XOMZ", "NVDL", "AMDL", "CONL", 
        "PTIR", "MULL", "FBL", "INTW", "TSLR", "BABX", "NVD", "MSFL", "NBIL", 
        "MVLL", "RDTL", "MRAL", "AMZZ", "TSDD", "TSMU", "VRTL", "CRWL", "IONL", 
        "SMCL", "NOWL", "DLLL", "AVGU", "AAPB", "UBRL", "CONI", "TSL", "QCML", 
        "PDDL", "RVNL", "MSTP", "GOU", "LCDL", "ISUL", "MSDD", "ETRL", "BULX", 
        "TSLQ", "APPX", "MQQQ", "SARK", "NVDS", "TARK", "QQQP", "SPYQ", "FLYT", 
        "AAOX", "AMZO", "APLX", "APLZ", "ARCX", "ASTX", "BEX", "BEZ", "CEGX", 
        "CLSX", "CLSZ", "COHX", "COZX", "CRDU", "CRMX", "CSEX", "CWVX", "DOGD", 
        "ENPX", "GEVX", "HLXX", "IBX", "IREX", "IREZ", "JOBX", "LABX", "LEUX", 
        "LITX", "LRCU", "MDBX", "NBIZ", "NEBX", "NNEX", "NVTX", "ONDU", "OPEX", 
        "PATX", "PONX", "QBTX", "QUBX", "RGTU", "SMQ", "SMU", "SMZ", "SNPX", 
        "SNXX", "SRPU", "TEMT", "UNX", "UPSX", "USAX", "VOYX", "WDCX", "WULX", 
        "IRE", "MSTX", "ORCX", "RKLX", "IONX", "OKLL", "SMCX", "HIMZ", "LLYX", 
        "RGTX", "SOFX", "PLTZ", "NVOX", "SMST", "RGTZ", "MST", "RIOX", "BMNZ", 
        "QPUX", "SOUX", "HOOX", "IONZ", "SMCZ", "QBTZ", "QSU", "HOOZ", "RCAX", 
        "OKLS", "AVXX", "VSTL", "OSCX", "DKNX", "ANEL", "LMNX", "CVNX", "DAMD", 
        "MPL", "RKLZ", "BU", "ASTN", "AVGX", "COPZ", "DRNL", "LNOK", "LUNL", 
        "MRNX", "ONDL", "PLU", "RKTL", "ZETX", "NVDX", "MSTU", "TSLT", "MSTZ", 
        "TSLZ", "GOOX", "NFLU", "BTCL", "BTCZ", "NVDQ", "MSFX", "ETU", "AAPX", 
        "AFRU", "APHU", "BMNU", "CCUP", "CIFU", "CORD", "CRCD", "CRWU", "DJTU", 
        "EOSU", "FGRU", "GLXU", "GMEU", "KTUP", "PAAU", "RDWU", "ROBN", "SBTU", 
        "SMUP", "SNDU", "SNOU", "SOLX", "TTDU", "XRPK", "MSOX", "AALG", "ABNG", 
        "ADBG", "ALBG", "AMDG", "ARMG", "ASMG", "AVGG", "AXPG", "BAIG", "BEG", 
        "BLSG", "BMNG", "BOEG"
    ]

    search_pool = list(set(user_essential_list))
    # 블랙리스트 재점검 (BULZ와 혼동될 만한 대형주 제외)
    blacklist = ["GOOGL", "GOOG", "FBTC", "ERO", "FETH"]

    final_results = []
    print(f"🚀 {len(search_pool)}개 종목 전수 조사 시작...")

    for ticker in search_pool:
        if ticker in blacklist: continue
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            aum = info.get('totalAssets') or info.get('marketCap')
            
            # $10MM 이상이거나 필수 리스트에 있는 경우 모두 허용
            if not aum or (aum < 10_000_000 and ticker not in user_essential_list):
                continue

            name = info.get('longName', ticker)
            
            # 키워드 필터링 대폭 강화 (ETN, MicroSectors 등 포함)
            lev_keywords = ['Leveraged', 'Bull', 'Bear', '2x', '3x', 'Short', 'Ultra', 
                            'Inverse', 'Strategy', 'Double', 'Triple', 'ETN', 'MicroSectors']
            
            is_valid = any(k.lower() in name.lower() for k in lev_keywords) or ticker in user_essential_list
            
            if is_valid:
                final_results.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": round(aum / 1_000_000, 2)
                })
                print(f"✅ {ticker} ($ {aum/1_000_000:.1f}MM) 수집 완료")
        except:
            continue

    final_results = sorted(final_results, key=lambda x: x['aum'], reverse=True)

    # 저장 직전 개수 확인 로그
    print(f"📦 최종 저장할 종목 수: {len(final_results)}개")

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    scrap_final_verified()
