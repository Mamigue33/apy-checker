#!/usr/bin/env python3
import socket, sys, ssl, time, os, urllib.request, subprocess, json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

os.system('clear')

def banner():
    print("\033[1;31m")
    print("  ╔══════════════════════════════════════════════════════════════════╗")
    print("  ║                    APY@ CHECKER 😈  v4.0                         ║")
    print("  ║           Scanner Profissional | SNI | Domínios | IP             ║")
    print("  ╚══════════════════════════════════════════════════════════════════╝")
    print("\033[0m")
    print("\033[1;36m" + "=" * 70 + "\033[0m")
    print("\033[1;33m              🔥 FERRAMENTA COMPLETA DE ANÁLISE 🔥\033[0m")
    print("\033[1;36m" + "=" * 70 + "\033[0m\n")

def menu():
    print("\033[1;36m╔════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;36m║                         📋 MENU PRINCIPAL 📋                     ║\033[0m")
    print("\033[1;36m╠════════════════════════════════════════════════════════════════╣\033[0m")
    print("\033[1;33m║  [1] 🔍 Scanner de Domínios                                     ║\033[0m")
    print("\033[1;36m║  [2] 🌐 Scanner de Múltiplas SNI                                ║\033[0m")
    print("\033[1;35m║  [3] 📡 Scanner de IP Address                                   ║\033[0m")
    print("\033[1;33m║  [4] 📊 Scanner de Tráfego de SNI                               ║\033[0m")
    print("\033[1;36m║  [5] 🔎 Pesquisar Lista de SNI Online                           ║\033[0m")
    print("\033[1;35m║  [6] 🐌 Scanner de SlowDNS                                      ║\033[0m")
    print("\033[1;33m║  [7] 🔗 Scanner de SNI Associadas                               ║\033[0m")
    print("\033[1;36m║  [8] 🌍 Scanner de Internet da SNI                              ║\033[0m")
    print("\033[1;35m║  [9] 🏆 Testar Várias SNI + Top 3 + Tráfego                     ║\033[0m")
    print("\033[1;33m║  [10] 💾 Download de Lista de SNI                               ║\033[0m")
    print("\033[1;31m║  [0] ❌ Sair                                                    ║\033[0m")
    print("\033[1;36m╚════════════════════════════════════════════════════════════════╝\033[0m")

def scan_dominios():
    print("\n\033[1;34m🔍 SCANNER DE DOMÍNIOS\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio base: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Domínio inválido!\033[0m")
        return
    subs = ['www', 'mail', 'ftp', 'dev', 'api', 'blog', 'admin', 'test', 'vpn', 'webmail', 'cloud', 'app', 'login', 'secure', 'm', 'mobile', 'shop', 'cdn', 'assets', 'download']
    print(f"\n📊 Escaneando {len(subs)} subdomínios...\n")
    for sub in subs:
        alvo = f"{sub}.{dominio}"
        try:
            ip = socket.gethostbyname(alvo)
            print(f"\033[32m✓ {alvo:<35} -> {ip}\033[0m")
        except:
            print(f"\033[90m✗ {alvo:<35}\033[0m")

def scan_multiplas_sni():
    print("\n\033[1;34m🌐 SCANNER DE MÚLTIPLAS SNI\033[0m")
    dominios = input("\033[1;33m📝 Digite os domínios separados por vírgula: \033[0m").strip()
    if not dominios:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    lista = [d.strip() for d in dominios.split(',')]
    print(f"\n📊 Analisando {len(lista)} SNIs...\n")
    for dominio in lista:
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((dominio, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=dominio) as ssock:
                    print(f"\033[32m✓ {dominio:<35} -> TLS: {ssock.version()}\033[0m")
        except:
            print(f"\033[90m✗ {dominio:<35}\033[0m")

def scan_ip():
    print("\n\033[1;34m📡 SCANNER DE IP ADDRESS\033[0m")
    ip = input("\033[1;33m🔢 Digite o IP: \033[0m").strip()
    if not ip:
        print("\033[1;31m❌ IP inválido!\033[0m")
        return
    portas = [21,22,23,25,53,80,110,135,139,143,443,445,993,995,1433,3306,3389,5432,5900,6379,8080,8443,27017]
    print(f"\n📊 Escaneando portas em {ip}...\n")
    for porta in portas:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex((ip, porta)) == 0:
                print(f"\033[32m✓ Porta {porta} ABERTA\033[0m")
            s.close()
        except:
            pass

def scan_trafego_sni():
    print("\n\033[1;34m📊 SCANNER DE TRÁFEGO DE SNI\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    try:
        start = time.time()
        req = urllib.request.Request(f"https://{dominio}/", headers={'User-Agent': 'APY@'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            dados = resp.read(102400)
            tempo = time.time() - start
            vel = (len(dados) * 8) / (tempo * 1024)
            print(f"\n\033[32m✅ Domínio: {dominio}\033[0m")
            print(f"📡 Velocidade: {round(vel, 2)} Kbps")
            print(f"💾 Dados: {round(len(dados)/1024, 2)} KB")
            print(f"⏱️ Tempo: {round(tempo*1000, 2)} ms")
    except Exception as e:
        print(f"\033[1;31m❌ Erro: {str(e)[:50]}\033[0m")

def pesquisar_sni_online():
    print("\n\033[1;34m🔎 PESQUISAR LISTA DE SNI ONLINE\033[0m")
    print("\033[1;33m[1] Usar lista padrão\033[0m")
    print("\033[1;33m[2] Digitar lista manual\033[0m")
    op = input("\n👉 Escolha: ").strip()
    snis = []
    if op == '1':
        snis = ['google.com', 'facebook.com', 'youtube.com', 'github.com', 'cloudflare.com', 'amazon.com', 'microsoft.com', 'netflix.com', 'twitter.com', 'instagram.com']
    else:
        texto = input("📝 Digite os domínios (separados por vírgula): ").strip()
        snis = [s.strip() for s in texto.split(',')]
    print(f"\n📊 Verificando {len(snis)} SNIs...\n")
    for sni in snis:
        try:
            socket.gethostbyname(sni)
            print(f"\033[32m✓ {sni:<35} ONLINE\033[0m")
        except:
            print(f"\033[90m✗ {sni:<35} OFFLINE\033[0m")

def scan_slowdns():
    print("\n\033[1;34m🐌 SCANNER DE SLOWDNS\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    subdominios = ['ns1', 'ns2', 'dns1', 'dns2', 'ns', 'dns', 'ns0', 'dns0']
    print(f"\n📊 Testando SlowDNS para {dominio}...\n")
    for sub in subdominios:
        alvo = f"{sub}.{dominio}"
        try:
            start = time.time()
            socket.gethostbyname(alvo)
            tempo = (time.time() - start) * 1000
            if tempo > 500:
                print(f"\033[33m⚠️ {alvo:<35} -> {round(tempo, 2)}ms (LENTO)\033[0m")
            else:
                print(f"\033[32m✓ {alvo:<35} -> {round(tempo, 2)}ms\033[0m")
        except:
            print(f"\033[90m✗ {alvo:<35}\033[0m")

def scan_sni_associadas():
    print("\n\033[1;34m🔗 SCANNER DE SNI ASSOCIADAS\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio base: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    associadas = [f"www.{dominio}", f"mail.{dominio}", f"ftp.{dominio}", f"dev.{dominio}", f"api.{dominio}", f"blog.{dominio}", f"admin.{dominio}", f"test.{dominio}", f"vpn.{dominio}", f"cloud.{dominio}", f"app.{dominio}", f"login.{dominio}", f"secure.{dominio}", f"cdn.{dominio}"]
    print(f"\n📊 Verificando SNIs associadas a {dominio}...\n")
    for sni in associadas:
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((sni, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=sni) as ssock:
                    print(f"\033[32m✓ {sni:<35} ATIVA - {ssock.version()}\033[0m")
        except:
            print(f"\033[90m✗ {sni:<35}\033[0m")

def scan_internet_sni():
    print("\n\033[1;34m🌍 SCANNER DE INTERNET DA SNI\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    try:
        ip = socket.gethostbyname(dominio)
        print(f"\n\033[32m✅ Domínio: {dominio}\033[0m")
        print(f"🔢 IP: {ip}")
        cmd = subprocess.run(['ping', '-c', '3', ip], capture_output=True, text=True)
        print(f"\n📡 TESTE DE LATÊNCIA:\n{cmd.stdout[-200:]}")
    except Exception as e:
        print(f"\033[1;31m❌ Erro: {e}\033[0m")

def testar_varias_sni():
    print("\n\033[1;34m🏆 TESTAR VÁRIAS SNI + TOP 3 + TRÁFEGO\033[0m")
    dominio = input("\033[1;33m🌐 Digite o domínio base: \033[0m").strip()
    if not dominio:
        print("\033[1;31m❌ Inválido!\033[0m")
        return
    subs = ['www', 'mail', 'api', 'blog', 'admin', 'dev', 'test', 'app', 'cloud', 'login', 'secure', 'cdn']
    snis = [dominio] + [f"{s}.{dominio}" for s in subs]
    resultados = []
    print(f"\n📊 Analisando {len(snis)} SNIs...\n")
    for sni in snis:
        try:
            start = time.time()
            ctx = ssl.create_default_context()
            with socket.create_connection((sni, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=sni) as ssock:
                    lat = round((time.time()-start)*1000, 2)
                    try:
                        req = urllib.request.Request(f"https://{sni}/", headers={'User-Agent': 'APY@'})
                        with urllib.request.urlopen(req, timeout=2) as resp:
                            dados = resp.read(30000)
                            vel = round((len(dados)*8)/((time.time()-start)*1024), 2)
                    except:
                        vel = 0
                    score = round(max(0, 100 - lat/10) + vel/10, 2)
                    resultados.append({'sni': sni, 'lat': lat, 'vel': vel, 'tls': ssock.version(), 'score': score})
                    print(f"\033[32m✓ {sni:<35} [{lat}ms] [{vel}Kbps]\033[0m")
        except:
            print(f"\033[90m✗ {sni:<35}\033[0m")
    if resultados:
        resultados.sort(key=lambda x: x['score'], reverse=True)
        print("\n\033[1;33m" + "="*70 + "\033[0m")
        print("\033[1;33m🏆 TOP 3 SNIs COM MELHOR DESEMPENHO 🏆\033[0m")
        print("\033[1;33m" + "="*70 + "\033[0m")
        for i, r in enumerate(resultados[:3], 1):
            print(f"\n\033[1;33m{i}º - \033[1;37m{r['sni']}\033[0m")
            print(f"   📍 Latência: \033[32m{r['lat']}ms\033[0m")
            print(f"   📡 Velocidade: \033[32m{r['vel']} Kbps\033[0m")
            print(f"   🔒 TLS: \033[32m{r['tls']}\033[0m")
            print(f"   📊 Score: \033[33m{r['score']}/100\033[0m")
        nome = f"apy_top3_{dominio}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(nome, 'w') as f:
            f.write(f"<h1>APY@ TOP 3 Report</h1><p>{dominio}</p><p>{datetime.now()}</p><p>SNIs ativas: {len(resultados)}</p>")
        print(f"\n\033[32m✅ Relatório salvo: {nome}\033[0m")

def download_sni_lista():
    print("\n\033[1;34m💾 DOWNLOAD DE LISTA DE SNI\033[0m")
    url = input("\033[1;33m🔗 Digite a URL da lista (raw): \033[0m").strip()
    if not url:
        print("\033[1;31m❌ URL inválida!\033[0m")
        return
    try:
        resposta = urllib.request.urlopen(url, timeout=10)
        conteudo = resposta.read().decode('utf-8')
        nome = f"sni_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(nome, 'w') as f:
            f.write(conteudo)
        print(f"\n\033[32m✅ Lista salva: {nome}\033[0m")
        linhas = conteudo.split('\n')
        print(f"📊 Total de SNIs: {len(linhas)}")
    except Exception as e:
        print(f"\033[1;31m❌ Erro ao baixar: {e}\033[0m")

def main():
    banner()
    menu()
    try:
        opcao = input("\n\033[1;33m👉 Escolha uma opção: \033[0m").strip()
        if opcao == '0':
            print("\n\033[1;31m❌ Saindo... Até mais! 👋\033[0m")
            return
        elif opcao == '1':
            scan_dominios()
        elif opcao == '2':
            scan_multiplas_sni()
        elif opcao == '3':
            scan_ip()
        elif opcao == '4':
            scan_trafego_sni()
        elif opcao == '5':
            pesquisar_sni_online()
        elif opcao == '6':
            scan_slowdns()
        elif opcao == '7':
            scan_sni_associadas()
        elif opcao == '8':
            scan_internet_sni()
        elif opcao == '9':
            testar_varias_sni()
        elif opcao == '10':
            download_sni_lista()
        else:
            print("\033[1;31m❌ Opção inválida!\033[0m")
            return
        input("\n\033[1;33m\n👉 Pressione ENTER para continuar...\033[0m")
        main()
    except KeyboardInterrupt:
        print("\n\033[1;31m❌ Programa interrompido!\033[0m")
    except EOFError:
        print("\n\033[1;31m❌ Entrada inválida! Execute novamente.\033[0m")

if __name__ == "__main__":
    main()
