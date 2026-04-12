import yfinance as yf
import json
import time

def scrap_comprehensive_leverage_etfs():
    # 1. 사용자가 요청한 모든 필수 티커 리스트 (누락 방지 마스터 명단)
    # TQQQ부터 ABNG까지 요청하신 모든 티커를 포함합니다.
    user_essential_list = [
        "TQQQ", "FNGO", "FNGD", "QLD", "SSO", "UPRO", "SQQQ", "AGQ", "USD", "SH", "UGL", "SCO", "PSQ", "ROM", "UDOW", "UYG", "UCO", "SDS", "SPXU", "DDM", "BOIL", "BITU", "QID", "URTY", "UVXY", "TBT", "UWM", "ETHT", "SBIT", "SVXY", "SDOW", "KOLD", "BITI", "RWM", "CRCA", "ZSL", "MVV", "DOG", "SJB", "GLL", "TBF", "DIG", "SRTY", "ETHD", "BIB", "RXL", "UBT", "TWM", "URE", "DXD", "EUO", "YCL", "UYM", "URSP", "EET", "YCS", "UXI", "UMDD", "EFO", "QQUP", "EFZ", "UPW", "UJB", "SAA", "SLON", "TTT", "SEF", "SKF", "SSG", "DUG", "TBX", "SRS", "SETH", "UST", "EPV", "EEV", "EZJ", "EUM", "UGE", "UPV", "REK", "UCC", "PST", "XPP", "NVDB", "SCC", "LTL", "EWV", "FXP", "SIJ", "ULE", "REW", "SZK", "QQXL", "SDP", "YXI", "UBR", "SBB", "PLTA", "RXD", "MYY", "UCYB", "SMN", "BZQ", "BIS", "COIA", "SMDD", "SDD", "EFU", "QQDN", "SKYU", "MZZ", "TSLI", "SOXL", "SPXL", "TSLL", "TECL", "TMF", "FAS", "SOXS", "TNA", "KORU", "NUGT", "MUU", "GGLL", "YINN", "MSFU", "JNUG", "NVDU", "NAIL", "DPST", "LABU", "DFEN", "SPXS", "PLTU", "TSMX", "METU", "AMZU", "TZA", "GUSH", "SPDN", "ERX", "CWEB", "SPUU", "TMV", "EDC", "AVL", "NFXL", "AAPU", "BRZU", "FAZ", "CURE", "YANG", "FNGG", "CHAU", "DRIP", "LABD", "WEBL", "TECS", "QQQU", "TSLS", "DUST", "MIDU", "HIBL", "EURL", "INDL", "URAA", "DRN", "DUSL", "UTSL", "ERY", "AMUU", "BRKU", "PLTD", "TYD", "JDST", "MUD", "DRV", "RETL", "UBOT", "QQQD", "EDZ", "MEXX", "HIBS", "ORCU", "NVDD", "AAPD", "AIBU", "LINT", "WANT", "ORCS", "TPOR", "AMDD", "GGLS", "WEBS", "ELIL", "PILL", "AMZD", "LMTL", "TYO", "METD", "AVS", "SHPU", "MRVU", "MSFD", "LMBO", "NFXS", "AIBD", "TEXU", "ASMU", "TSXU", "HODU", "CSCL", "QCMU", "TTXD", "TBXU", "QCMD", "SHPD", "BABU", "CONX", "TTXU", "ELIS", "SOFA", "TSMZ", "FRDU", "FRDD", "CSCS", "REKT", "TSXD", "LMTS", "BRKD", "ADBU", "BOED", "BOEU", "PALD", "PALU", "PYPU", "TXNU", "UNHU", "XOMX", "XOMZ", "NVDL", "AMDL", "CONL", "PTIR", "MULL", "FBL", "INTW", "TSLR", "BABX", "NVD", "MSFL", "NBIL", "MVLL", "RDTL", "MRAL", "AMZZ", "TSDD", "TSMU", "VRTL", "CRWL", "IONL", "SMCL", "NOWL", "DLLL", "AVGU", "AAPB", "UBRL", "CONI", "TSL", "QCML", "PDDL", "RVNL", "MSTP", "GOU", "LCDL", "ISUL", "MSDD", "ETRL", "BULX", "TSLQ", "APPX", "MQQQ", "SARK", "NVDS", "TARK", "QQQP", "SPYQ", "FLYT", "AAOX", "AMZO", "APLX", "APLZ", "ARCX", "ASTX", "BEX", "BEZ", "CEGX", "CLSX", "CLSZ", "COHX", "COZX", "CRDU", "CRMX", "CSEX", "CWVX", "DOGD", "ENPX", "GEVX", "HLXX", "IBX", "IREX", "IREZ", "JOBX", "LABX", "LEUX", "LITX", "LRCU", "MDBX", "NBIZ", "NEBX", "NNEX", "NVTX", "ONDU", "OPEX", "PATX", "PONX", "QBTX", "QUBX", "RGTU", "SMQ", "SMU", "SMZ", "SNPX", "SNXX", "SRPU", "TEMT", "UNX", "UPSX", "USAX", "VOYX", "WDCX", "WULX", "IRE", "MSTX", "ORCX", "RKLX", "IONX", "OKLL", "SMCX", "HIMZ", "LLYX", "RGTX", "SOFX", "PLTZ", "NVOX", "SMST", "RGTZ", "MST", "RIOX", "BMNZ", "QPUX", "SOUX", "HOOX", "IONZ", "SMCZ", "QBTZ", "QSU", "HOOZ", "RCAX", "OKLS", "AVXX", "VSTL", "OSCX", "DKNX", "ANEL", "LMNX", "CVNX", "DAMD", "MPL", "RKLZ", "BU", "ASTN", "AVGX", "COPZ", "DRNL", "LNOK", "LUNL", "MRNX", "ONDL", "PLU", "RKTL", "ZETX", "NVDX", "MSTU", "TSLT", "MSTZ", "TSLZ", "GOOX", "NFLU", "BTCL", "BTCZ", "NVDQ", "MSFX", "ETU", "AAPX", "AFRU", "APHU", "BMNU", "CCUP", "CIFU", "CORD", "CRCD", "CRWU", "DJTU", "EOSU", "FGRU", "GLXU", "GMEU", "KTUP", "PAAU", "RDWU", "ROBN", "SBTU", "SMUP", "SNDU", "SNOU", "SOLX", "TTDU", "XRPK", "MSOX", "AALG", "ABNG", "ADBG", "ALBG", "AMDG", "ARMG", "ASMG", "AVGG", "AXPG", "BAIG", "BEG", "BLSG", "BMNG", "BOEG"
    ]

    # 2. 신규 상장 대비 자동 조합 (Prefix + Base)
    # 기존에 잘 작동하던 신규 탐색 로직은 그대로 유지합니다.
    bases = ["QQQ", "SPY", "SOX", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "META", "COIN", "BTC", "ETH"]
    prefixes = ["T", "S", "U", "D", "L", "F"]
    generated = [p + b for p in prefixes for b in bases] + [b + "L" for b in bases] + [b + "S" for b in bases]

    # 3. 중복 제거 및 최종 탐색 풀
    search_pool = list(set(user_essential_list + generated))
    
    # 4. 개별 주식 차단 리스트 (GOOGL, FBTC 등)
    # 일반 현물 ETF나 대형주가 레버리지 리스트에 섞이지 않게 합니다.
    blacklist = ["GOOGL", "GOOG", "FBTC", "ERO", "FETH", "AAPL", "MSFT", "TSLA", "NVDA", "AMZN", "META"]

    final_results = []
    print(f"📡 총 {len(search_pool)}개 종목 전수 조사 시작...")

    for ticker in search_pool:
        if ticker in blacklist: continue # 블랙리스트 차단

        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM 데이터 확보 ($10MM 이상 필터)
            aum = info.get('totalAssets') or info.get('marketCap')
            if not aum or aum < 10_000_000: continue

            name = info.get('longName', ticker)
            
            # 레버리지 검증 키워드 (이름에 포함되어야 함)
            lev_keywords = [
                'Leveraged', 'Bull', 'Bear', '2x', '3x', 'Short', 'Ultra', 
                'Inverse', 'Daily', 'Strategy', 'Double', 'Triple', 'Long'
            ]
            
            is_leveraged = any(k.lower() in name.lower() for k in lev_keywords)
            
            # 필수 리스트에 포함되어 있거나, 레버리지 키워드가 검증된 경우만 추가
            if is_leveraged or ticker in user_essential_list:
                final_results.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": round(aum / 1_000_000, 2)
                })
                print(f"✅ 수집 성공: {ticker} - {name}")
            
            time.sleep(0.05)
        except:
            continue

    # 5. AUM 순 정렬
    final_results = sorted(final_results, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    
    print(f"🎉 업데이트 완료! 총 {len(final_results)}개의 유효 레버리지 종목을 찾았습니다.")

if __name__ == "__main__":
    scrap_comprehensive_leverage_etfs()
