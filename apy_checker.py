#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import sys
import ssl
import time
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

def banner():
    os.system('clear')
    print("\033[1;31m" + """
    ╔══════════════════════════════════════════════════════════╗
    ║     APY@ CHECKER 😈  v3.0 - SNI Traffic Analyzer        ║
    ║     Domain | Subdomain | SNI Scanner | Top 3 Traffic     ║
    ╚══════════════════════════════════════════════════════════╝
    """ + "\033[0m")

def resolve_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except:
        return None

def test_sni_connection(domain, port=443):
    try:
        start_time = time.time()
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                handshake_time = (time.time() - start_time) * 1000
                cert = ssock.getpeercert()
                return {
                    'domain': domain,
                    'status': 'active',
                    'latency_ms': round(handshake_time, 2),
                    'tls_version': ssock.version(),
                    'cert_subject': cert.get('subject', [[domain]])[0][0][1],
                    'port': port
                }
    except Exception as e:
        return {
            'domain': domain,
            'status': 'inactive',
            'error': str(e)[:50]
        }

def measure_traffic(domain, port=443, test_duration=2):
    try:
        import urllib.request
        url = f"https://{domain}/"
        start_time = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=test_duration) as response:
            data = response.read(1024 * 100)
            download_time = time.time() - start_time
            speed_kbps = (len(data) * 8) / (download_time * 1024) if download_time > 0 else 0
        return {
            'download_speed_kbps': round(speed_kbps, 2),
            'data_transfer_kb': round(len(data) / 1024, 2),
            'response_time_ms': round(download_time * 1000, 2)
        }
    except:
        return {
            'download_speed_kbps': 0,
            'data_transfer_kb': 0,
            'response_time_ms': 9999
        }

def scan_sni_domains(domain):
    sub_list = [
        "", "www", "mail", "ftp", "dev", "api", "blog", "admin", "test", "vpn",
        "webmail", "cloud", "app", "login", "secure", "m", "mobile", "shop",
        "cdn", "assets", "download", "upload", "database", "backup", "beta",
        "auth", "dashboard", "panel", "smtp", "imap", "chat", "forum",
        "community", "meet", "team", "rest", "graphql", "account", "user",
        "profile", "analytics", "logs", "monitor", "live", "storage"
    ]
    sni_list = []
    for sub in sub_list:
        if sub:
            sni_list.append(f"{sub}.{domain}")
        else:
            sni_list.append(domain)
    sni_list.extend([
        f"api.{domain}", f"ws.{domain}", f"socket.{domain}",
        f"stream.{domain}", f"data.{domain}", f"sync.{domain}"
    ])
    return list(set(sni_list))

def analyze_sni_traffic(domain):
    print("\033[1;36m[>] Gerando lista de SNIs para analise...\033[0m")
    sni_list = scan_sni_domains(domain)
    print(f"\033[1;33m[!] Total de SNIs a analisar: {len(sni_list)}\033[0m")
    results = []
    total = len(sni_list)
    print("\n\033[1;36m[>] Analisando trafego e latencia das SNIs...\033[0m\n")
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_sni = {executor.submit(test_sni_connection, sni): sni for sni in sni_list}
        for idx, future in enumerate(as_completed(future_to_sni), 1):
            sni = future_to_sni[future]
            try:
                result = future.result()
                if result['status'] == 'active':
                    traffic = measure_traffic(sni)
                    result.update(traffic)
                    results.append(result)
                    progress = int((idx / total) * 50)
                    bar = "#" * progress + "." * (50 - progress)
                    print(f"\r\033[32m[{bar}] {idx}/{total} - Ativa: {sni} (Lat: {result['latency_ms']}ms)\033[0m", end="")
                else:
                    print(f"\r\033[90m[{idx}/{total}] Inativa: {sni}\033[0m", end="")
            except:
                pass
    print("\n")
    for r in results:
        latency_score = max(0, 100 - (r['latency_ms'] / 10))
        speed_score = min(100, r.get('download_speed_kbps', 0) / 10)
        r['score'] = round((latency_score * 0.6) + (speed_score * 0.4), 2)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

def show_top_3_traffic(results):
    print("\n" + "="*70)
    print("\033[1;33m🏆 TOP 3 SNIs COM MAIOR TRAFEGO/DADOS 🏆\033[0m")
    print("="*70)
    if len(results) == 0:
        print("\033[1;31m[-] Nenhuma SNI ativa encontrada!\033[0m")
        return
    medals = ["🥇", "🥈", "🥉"]
    colors = ["\033[1;33m", "\033[1;36m", "\033[1;35m"]
    for i in range(min(3, len(results))):
        sni = results[i]
        print(f"\n{colors[i]}{medals[i]} #{i+1} - {sni['domain']}\033[0m")
        print(f"   📍 Latencia: {sni['latency_ms']}ms")
        print(f"   📡 Velocidade Download: {sni.get('download_speed_kbps', 0)} Kbps")
        print(f"   💾 Dados Transferidos: {sni.get('data_transfer_kb', 0)} KB")
        print(f"   🔒 TLS Versao: {sni.get('tls_version', 'N/A')}")
        print(f"   📊 Score Geral: {sni['score']}/100")
        print(f"   🎯 Status: \033[32mATIVA - Gerando trafego\033[0m")
        traffic_bar = int(sni.get('download_speed_kbps', 0) / 10)
        traffic_bar = min(30, max(0, traffic_bar))
        bar = "🚀" * traffic_bar + "💨" * (30 - traffic_bar)
        print(f"   📈 Trafego: {bar}")

def generate_traffic_report(domain, results, filename=None):
    if not filename:
        filename = f"apy_traffic_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>APY@ CHECKER - Relatorio de Trafego SNI - {domain}</title>
    <style>
        body {{ font-family: 'Courier New', monospace; margin: 20px; background: #0a0a0a; color: #0f0; }}
        h1 {{ color: #ff4444; text-align: center; }}
        h2 {{ color: #ff8800; }}
        .top3 {{ background: #1a1a1a; padding: 15px; border-radius: 10px; margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #00ff00; padding: 10px; text-align: left; }}
        th {{ background: #1a1a1a; color: #ff8800; }}
        .score {{ font-weight: bold; }}
        .high {{ color: #00ff00; }}
        .medium {{ color: #ffff00; }}
        .low {{ color: #ff4444; }}
    </style>
</head>
<body>
    <h1>📊 APY@ CHECKER - Analise de Trafego SNI</h1>
    <p><strong>Dominio Base:</strong> {domain}</p>
    <p><strong>Data da Analise:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Total de SNIs Ativas:</strong> {len(results)}</p>
    <div class="top3">
        <h2>🏆 TOP 3 SNIs - Melhor Trafego</h2>
""")
        medals_html = ["🥇 1º Lugar", "🥈 2º Lugar", "🥉 3º Lugar"]
        for i in range(min(3, len(results))):
            sni = results[i]
            f.write(f"""
        <div style="margin: 20px 0; padding: 10px; border-left: 4px solid {'#ffd700' if i==0 else '#c0c0c0' if i==1 else '#cd7f32'};">
            <h3>{medals_html[i]}: {sni['domain']}</h3>
            <p>📡 Latencia: {sni['latency_ms']}ms | ⚡ Velocidade: {sni.get('download_speed_kbps', 0)} Kbps</p>
            <p>💾 Dados: {sni.get('data_transfer_kb', 0)} KB | 🔒 TLS: {sni.get('tls_version', 'N/A')}</p>
            <p>📊 Score: {sni['score']}/100</p>
        </div>
""")
        f.write("""    </div>
    <h2>📋 Todas as SNIs Ativas</h2>
    <table>
        <tr><th>SNI</th><th>Latencia (ms)</th><th>Velocidade (Kbps)</th><th>Dados (KB)</th><th>Score</th></tr>
""")
        for sni in results:
            score_class = "high" if sni['score'] > 70 else "medium" if sni['score'] > 40 else "low"
            f.write(f"""
        <tr>
            <td>{sni['domain']}</td>
            <td>{sni['latency_ms']}</td>
            <td>{sni.get('download_speed_kbps', 0)}</td>
            <td>{sni.get('data_transfer_kb', 0)}</td>
            <td class="{score_class}">{sni['score']}</td>
        </tr>
""")
        f.write("""    </table>
</body>
</html>""")
    print(f"\n\033[32m[+] Relatorio de trafego salvo: {filename}\033[0m")
    return filename

def main():
    banner()
    print("\033[1;33m[1] Scan Completo (Subdominios + SNI + Trafego + Top 3)")
    print("[2] Apenas Analise de Trafego SNI (Top 3)")
    print("[3] Scan Rapido (Apenas SNIs ativas)")
    print("[0] Sair\033[0m")
    choice = input("\n\033[1;36m[?] Escolha uma opcao: \033[0m").strip()
    if choice == "0":
        print("\033[1;31m[-] Saindo...\033[0m")
        sys.exit(0)
    target = input("\033[1;33m[?] Digite o dominio alvo (ex: google.com): \033[0m").strip()
    if not target:
        print("\033[1;31m[-] Dominio invalido!\033[0m")
        sys.exit(1)
    print(f"\n\033[1;36m[>] Analisando trafego SNI para: {target}\033[0m")
    results = analyze_sni_traffic(target)
    if len(results) == 0:
        print("\033[1;31m[-] Nenhuma SNI ativa encontrada!\033[0m")
        sys.exit(1)
    show_top_3_traffic(results)
    report_file = generate_traffic_report(target, results)
    print("\n" + "="*70)
    print(f"\033[1;32m[+] ANALISE CONCLUIDA!\033[0m")
    print(f"\033[1;32m[+] Total de SNIs ativas: {len(results)}\033[0m")
    print(f"\033[1;32m[+] Relatorio HTML: {report_file}\033[0m")
    print("\033[1;33m[!] As 3 melhores SNIs sao as que geram mais trafego!\033[0m")
    print("="*70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m\n[-] Scan interrompido pelo usuario!\033[0m")
        sys.exit(0)
