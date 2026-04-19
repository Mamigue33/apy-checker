#!/usr/bin/env python3
import socket import sys import ssl import time 
import os from datetime import datetime from 
concurrent.futures import ThreadPoolExecutor, 
as_completed def clear():
    os.system('clear') def banner(): clear() 
    print("\033[1;31m") print(" 
    ╔════════════════════════════════════════════════════════╗") 
    print(" ║ APY@ CHECKER 😈 v3.0 ║") print(" ║ 
    Domain | SNI Scanner | Top 3 Traffic ║") 
    print(" 
    ╚════════════════════════════════════════════════════════╝") 
    print("\033[0m") print("\033[1;36m" + "=" * 60 
    + "\033[0m") print("\033[1;33m 🔥 FERRAMENTA 
    PROFISSIONAL 🔥\033[0m") print("\033[1;36m" + 
    "=" * 60 + "\033[0m\n")
def resolve_ip(domain): try: return 
        socket.gethostbyname(domain)
    except: return None def test_sni(domain): try: 
        start = time.time() ctx = 
        ssl.create_default_context() with 
        socket.create_connection((domain, 443), 
        timeout=5) as sock:
            with ctx.wrap_socket(sock, 
            server_hostname=domain) as ssock:
                lat = round((time.time() - start) * 
                1000, 2) return {'domain': domain, 
                'latency_ms': lat, 'status': 
                'active', 'tls': ssock.version()}
    except: return {'domain': domain, 'status': 
        'inactive'}
def measure_traffic(domain): try: import 
        urllib.request start = time.time() req = 
        urllib.request.Request(f"https://{domain}/", 
        headers={'User-Agent': 'Mozilla/5.0'}) with 
        urllib.request.urlopen(req, timeout=3) as 
        resp:
            data = resp.read(50000) speed = 
            (len(data) * 8) / ((time.time() - 
            start) * 1024) return {'speed_kbps': 
            round(speed, 2), 'data_kb': 
            round(len(data) / 1024, 2)}
    except: return {'speed_kbps': 0, 'data_kb': 0} 
def get_snis(domain):
    subs = ['www', 'mail', 'api', 'blog', 'admin', 
    'dev', 'test', 'app', 'cloud', 'login', 
    'secure', 'cdn', 'ftp', 'webmail', 'panel', 
    'dashboard', 'auth', 'account', 'user', 
    'support'] snis = [domain] + [f"{s}.{domain}" 
    for s in subs] return list(set(snis))
def analyze(domain): snis = get_snis(domain) 
    print(f"\033[1;34m📊 Analisando {len(snis)} 
    SNIs...\033[0m\n")
    
    results = [] total = len(snis)
    
    with ThreadPoolExecutor(max_workers=10) as ex: 
        futures = {ex.submit(test_sni, sni): sni 
        for sni in snis} for i, f in 
        enumerate(as_completed(futures), 1):
            r = f.result() if r['status'] == 
            'active':
                traffic = 
                measure_traffic(r['domain']) 
                r.update(traffic) results.append(r) 
                print(f"\r\033[32m[{i}/{total}] ✓ 
                ATIVA: {r['domain']:<35} 
                [{r['latency_ms']}ms]\033[0m")
            else: print(f"\r\033[90m[{i}/{total}] ✗ 
                INATIVA: {r['domain']:<35}\033[0m")
    
    for r in results: score = max(0, 100 - 
        (r['latency_ms'] / 10)) + 
        (r.get('speed_kbps', 0) / 10) r['score'] = 
        round(score, 2)
    
    results.sort(key=lambda x: x['score'], 
    reverse=True) return results
def show_top3(results): print("\n" + "\033[1;33m" + 
    "═" * 60 + "\033[0m") print("\033[1;33m 🏆 TOP 
    3 SNIs COM MELHOR DESEMPENHO 🏆\033[0m") 
    print("\033[1;33m" + "═" * 60 + "\033[0m\n")
    
    for i in range(min(3, len(results))): r = 
        results[i] medal = ["🥇 1º", "🥈 2º", "🥉 
        3º"][i] print(f"\033[1;33m{medal} 
        LUGAR:\033[0m 
        \033[1;37m{r['domain']}\033[0m") print(f" 
        📍 Latência: 
        \033[32m{r['latency_ms']}ms\033[0m") 
        print(f" 📡 Velocidade: 
        \033[32m{r.get('speed_kbps', 0)} 
        Kbps\033[0m") print(f" 💾 Dados: 
        \033[32m{r.get('data_kb', 0)} KB\033[0m") 
        print(f" 🔒 TLS: \033[32m{r.get('tls', 
        'N/A')}\033[0m") print(f" 📊 Score: 
        \033[33m{r['score']}/100\033[0m") print()
def main(): banner()
    
    print("\033[1;36m╔════════════════════════════════════════╗\033[0m") 
    print("\033[1;36m║ 📋 MENU PRINCIPAL ║\033[0m") 
    print("\033[1;36m╠════════════════════════════════════════╣\033[0m") 
    print("\033[1;33m║ [1] Scan Completo (SNI + 
    Tráfego) ║\033[0m") print("\033[1;36m║ [2] 
    Apenas Top 3 SNI ║\033[0m") print("\033[1;31m║ 
    [0] Sair ║\033[0m") 
    print("\033[1;36m╚════════════════════════════════════════╝\033[0m")
    
    try: opcao = input("\n\033[1;33m👉 Escolha: 
        \033[0m").strip() if opcao == "0":
            print("\n\033[1;31m❌ 
            Saindo...\033[0m") return
        
        alvo = input("\033[1;33m🌐 Domínio: 
        \033[0m").strip() if not alvo:
            print("\033[1;31m❌ Domínio 
            inválido!\033[0m") return
        
        print() resultados = analyze(alvo)
        
        if not resultados: print("\033[1;31m❌ 
            Nenhuma SNI ativa encontrada!\033[0m") 
            return
        
        show_top3(resultados)
        
        # Relatório
        nome = 
        f"apy_report_{alvo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html" 
        with open(nome, 'w') as f:
            f.write(f"<html><head><title>APY@ 
            Report</title></head><body>") 
            f.write(f"<h1>APY@ CHECKER - 
            Relatório</h1>") f.write(f"<p>Domínio: 
            {alvo}</p><p>Data: 
            {datetime.now()}</p>") 
            f.write(f"<p>SNIs ativas: 
            {len(resultados)}</p></body></html>")
        
        print(f"\033[32m✅ Relatório salvo: 
        {nome}\033[0m") print(f"\033[32m✅ Total 
        SNIs ativas: {len(resultados)}\033[0m")
        
    except KeyboardInterrupt: print("\n\033[31m❌ 
        Interrompido!\033[0m")
    except EOFError: print("\n\033[31m❌ Entrada 
        inválida! Execute novamente.\033[0m")
if __name__ == "__main__":
    main()
0

