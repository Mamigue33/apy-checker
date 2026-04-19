#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket import sys import ssl import time 
import os from datetime import datetime from 
concurrent.futures import ThreadPoolExecutor, 
as_completed def clear_screen():
    os.system('clear') def banner(): clear_screen() 
    print("\033[1;31m" + r""" 
    ╔══════════════════════════════════════════════════════════════════╗ 
    ║ ║ ║ █████╗ ██████╗ ██╗ ██╗ ██████╗██╗ 
    ██╗███████╗██╗ ║ ║ ██╔══██╗██╔══██╗╚██╗ ██╔╝ 
    ██╔════╝██║ ██╔╝██╔════╝██║ ║ ║ 
    ███████║██████╔╝ ╚████╔╝ ██║ █████╔╝ █████╗ ██║ 
    ║ ║ ██╔══██║██╔═══╝ ╚██╔╝ ██║ ██╔═██╗ ██╔══╝ 
    ╚═╝ ║ ║ ██║ ██║██║ ██║ ╚██████╗██║ 
    ██╗███████╗██╗ ║ ║ ╚═╝ ╚═╝╚═╝ ╚═╝ ╚═════╝╚═╝ 
    ╚═╝╚══════╝╚═╝ ║ ║ ║ ║ ███████╗██╗ ██╗██╗ 
    ██████╗ ║ ║ ██╔════╝╚██╗ ██╔╝██║ ╚════██╗ ║ ║ 
    █████╗ ╚████╔╝ ██║ █████╔╝ ║ ║ ██╔══╝ ╚██╔╝ ██║ 
    ██╔═══╝ ║ ║ ██║ ██║ ██║ ███████╗ ║ ║ ╚═╝ ╚═╝ 
    ╚═╝ ╚══════╝ ║ ║ ║ ║ Domain | Subdomain | SNI 
    Scanner | Top 3 ║ ║ v3.0 - Traffic Analyzer ║ ║ 
    ║ 
    ╚══════════════════════════════════════════════════════════════════╝ 
    """ + "\033[0m") print("\033[1;36m" + "=" * 70 
    + "\033[0m") print("\033[1;33m" + " 🔥 
    FERRAMENTA PROFISSIONAL DE ANÁLISE 🔥" + 
    "\033[0m") print("\033[1;36m" + "=" * 70 + 
    "\033[0m\n")
def resolve_ip(domain): try: return 
        socket.gethostbyname(domain)
    except: return None def 
test_sni_connection(domain, port=443):
    try: start_time = time.time() context = 
        ssl.create_default_context() with 
        socket.create_connection((domain, port), 
        timeout=5) as sock:
            with context.wrap_socket(sock, 
            server_hostname=domain) as ssock:
                handshake_time = (time.time() - 
                start_time) * 1000 cert = 
                ssock.getpeercert() return {
                    'domain': domain, 'status': 
                    'active', 'latency_ms': 
                    round(handshake_time, 2), 
                    'tls_version': ssock.version(), 
                    'cert_subject': 
                    cert.get('subject', 
                    [[domain]])[0][0][1], 'port': 
                    port
                }
    except: return {'domain': domain, 'status': 
        'inactive'}
def measure_traffic(domain, port=443, 
test_duration=2):
    try: import urllib.request url = 
        f"https://{domain}/" start_time = 
        time.time() req = 
        urllib.request.Request(url, 
        headers={'User-Agent': 'Mozilla/5.0'}) with 
        urllib.request.urlopen(req, 
        timeout=test_duration) as response:
            data = response.read(1024 * 100) 
            download_time = time.time() - 
            start_time speed_kbps = (len(data) * 8) 
            / (download_time * 1024) if 
            download_time > 0 else 0
        return { 'download_speed_kbps': 
            round(speed_kbps, 2), 
            'data_transfer_kb': round(len(data) / 
            1024, 2), 'response_time_ms': 
            round(download_time * 1000, 2)
        }
    except: return {'download_speed_kbps': 0, 
        'data_transfer_kb': 0, 'response_time_ms': 
        9999}
def scan_sni_domains(domain): subs = [ "", "www", 
        "mail", "ftp", "dev", "api", "blog", 
        "admin", "test", "vpn", "webmail", "cloud", 
        "app", "login", "secure", "m", "mobile", 
        "shop", "cdn", "assets", "download", 
        "upload", "database", "backup", "beta", 
        "auth", "dashboard", "panel", "smtp", 
        "imap", "chat", "forum", "community", 
        "meet", "team", "rest", "graphql", 
        "account", "user", "profile", "analytics", 
        "logs", "monitor", "live", "storage"
    ] snis = [] for sub in subs: 
        snis.append(f"{sub}.{domain}" if sub else 
        domain)
    return list(set(snis)) def 
analyze_sni_traffic(domain):
    print("\033[1;36m┌────────────────────────────────────────────────────────────────────┐\033[0m") 
    print(f"\033[1;36m│ 🔍 ANALISANDO SNIS PARA: 
    \033[1;33m{domain}\033[0m") 
    print("\033[1;36m└────────────────────────────────────────────────────────────────────┘\033[0m\n")
    
    sni_list = scan_sni_domains(domain) 
    print(f"\033[1;34m📊 Total de SNIs a analisar: 
    \033[1;33m{len(sni_list)}\033[0m\n")
    
    results = [] total = len(sni_list)
    
    with ThreadPoolExecutor(max_workers=10) as 
    executor:
        future_to_sni = 
        {executor.submit(test_sni_connection, sni): 
        sni for sni in sni_list}
        
        for idx, future in 
        enumerate(as_completed(future_to_sni), 1):
            result = future.result() if 
            result['status'] == 'active':
                traffic = 
                measure_traffic(result['domain']) 
                result.update(traffic) 
                results.append(result)
                
                # Barra de progresso
                percent = int((idx / total) * 40) 
                bar = "█" * percent + "░" * (40 - 
                percent) print(f"\r\033[32m[{bar}] 
                \033[1;33m{idx}/{total}\033[0m 
                \033[32m✓ ATIVA:\033[0m 
                {result['domain']:<35} 
                \033[36m[{result['latency_ms']}ms]\033[0m", 
                end="")
            else: percent = int((idx / total) * 40) 
                bar = "█" * percent + "░" * (40 - 
                percent) print(f"\r\033[90m[{bar}] 
                \033[1;33m{idx}/{total}\033[0m 
                \033[90m✗ INATIVA:\033[0m 
                {result['domain']:<35}\033[0m", 
                end="")
    
    print("\n\n\033[1;36m┌────────────────────────────────────────────────────────────────────┐\033[0m") 
    print(f"\033[1;32m│ ✅ ANÁLISE CONCLUÍDA! 
    \033[1;33m{len(results)} SNIs ativas 
    encontradas\033[0m") 
    print("\033[1;36m└────────────────────────────────────────────────────────────────────┘\033[0m\n")
    
    for r in results: latency_score = max(0, 100 - 
        (r['latency_ms'] / 10)) speed_score = 
        min(100, r.get('download_speed_kbps', 0) / 
        10) r['score'] = round((latency_score * 
        0.6) + (speed_score * 0.4), 2)
    
    results.sort(key=lambda x: x['score'], 
    reverse=True) return results
def show_top_3(results): print("\033[1;33m" + "╔" + 
    "═" * 68 + "╗\033[0m") print("\033[1;33m║" + " 
    " * 20 + "🏆 TOP 3 SNIs COM MELHOR DESEMPENHO 
    🏆" + " " * 20 + "║\033[0m") 
    print("\033[1;33m╚" + "═" * 68 + "╝\033[0m\n")
    
    medals = ["🥇 1º LUGAR", "🥈 2º LUGAR", "🥉 3º 
    LUGAR"] colors = ["\033[1;33m", "\033[1;36m", 
    "\033[1;35m"]
    
    for i in range(min(3, len(results))): sni = 
        results[i] print(colors[i] + "┌" + "─" * 66 
        + "┐\033[0m") print(f"{colors[i]}│ 
        {medals[i]}: 
        \033[1;37m{sni['domain']}\033[0m") 
        print(f"{colors[i]}├" + "─" * 66 + 
        "┤\033[0m") print(f"{colors[i]}│ 📍 
        Latência: 
        \033[1;32m{sni['latency_ms']}ms\033[0m") 
        print(f"{colors[i]}│ 📡 Velocidade: 
        \033[1;32m{sni.get('download_speed_kbps', 
        0)} Kbps\033[0m") print(f"{colors[i]}│ 💾 
        Dados: 
        \033[1;32m{sni.get('data_transfer_kb', 0)} 
        KB\033[0m") print(f"{colors[i]}│ 🔒 TLS: 
        \033[1;32m{sni.get('tls_version', 
        'N/A')}\033[0m") print(f"{colors[i]}│ 📊 
        Score: 
        \033[1;33m{sni['score']}/100\033[0m")
        
        # Barra de tráfego
        traffic_bar = int(min(30, max(0, 
        sni.get('download_speed_kbps', 0) / 10))) 
        bar = "🚀" * traffic_bar + "💨" * (30 - 
        traffic_bar) print(f"{colors[i]}│ 📈 
        Tráfego: {bar}\033[0m") print(colors[i] + 
        "└" + "─" * 66 + "┘\033[0m\n")
def main(): banner()
    
    print("\033[1;36m╔════════════════════════════════════════════════════════════════════╗\033[0m") 
    print("\033[1;36m║ 📋 MENU PRINCIPAL 📋 
    ║\033[0m") 
    print("\033[1;36m╠════════════════════════════════════════════════════════════════════╣\033[0m") 
    print("\033[1;33m║ [1] 🚀 Scan Completo 
    (Subdomínios + SNI + Tráfego + Top 3) 
    ║\033[0m") print("\033[1;36m║ [2] 📊 Apenas 
    Análise de Tráfego SNI (Top 3) ║\033[0m") 
    print("\033[1;35m║ [3] ⚡ Scan Rápido (Apenas 
    SNIs ativas) ║\033[0m") print("\033[1;31m║ [0] 
    ❌ Sair ║\033[0m") 
    print("\033[1;36m╚════════════════════════════════════════════════════════════════════╝\033[0m")
    
    try: choice = input("\n\033[1;33m👉 Escolha uma 
        opção: \033[0m").strip()
        
        if choice == "0": print("\n\033[1;31m❌ 
            Saindo... Até mais! 👋\033[0m") 
            sys.exit(0)
        
        target = input("\033[1;33m🌐 Digite o 
        domínio alvo (ex: google.com): 
        \033[0m").strip()
        
        if not target: print("\033[1;31m❌ Domínio 
            inválido!\033[0m") sys.exit(1)
        
        print() results = 
        analyze_sni_traffic(target)
        
        if len(results) == 0: print("\033[1;31m❌ 
            Nenhuma SNI ativa encontrada!\033[0m") 
            sys.exit(1)
        
        show_top_3(results)
        
        # Gerar relatório HTML
        filename = 
        f"apy_report_{target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html" 
        with open(filename, "w") as f:
            f.write(f"<html><head><title>APY@ 
            Report - 
            {target}</title></head><body>") 
            f.write(f"<h1>APY@ CHECKER - 
            Relatório</h1><p>Domínio: 
            {target}</p>") f.write(f"<p>Data: 
            {datetime.now()}</p><p>Total SNIs 
            ativas: {len(results)}</p>") 
            f.write("</body></html>")
        
        print("\033[1;36m╔════════════════════════════════════════════════════════════════════╗\033[0m") 
        print("\033[1;32m║ ✅ SCAN CONCLUÍDO! ✅ 
        ║\033[0m") 
        print("\033[1;36m╠════════════════════════════════════════════════════════════════════╣\033[0m") 
        print(f"\033[1;33m║ 📁 Relatório HTML: 
        \033[1;37m{filename}\033[0m") 
        print(f"\033[1;33m║ 🌐 Total de SNIs 
        ativas: \033[1;32m{len(results)}\033[0m") 
        print("\033[1;36m╚════════════════════════════════════════════════════════════════════╝\033[0m\n")
        
    except KeyboardInterrupt: print("\n\033[1;31m❌ 
        Scan interrompido pelo usuário!\033[0m") 
        sys.exit(0)
    except EOFError: print("\n\033[1;31m❌ Entrada 
        inválida! Por favor, execute 
        novamente.\033[0m") sys.exit(0)
if __name__ == "__main__":
    main()0

