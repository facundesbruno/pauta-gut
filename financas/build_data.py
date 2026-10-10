"""Gera financas/lancamentos.json a partir das transações transcritas de cada mês.
Para adicionar um mês: acrescente uma entrada em MESES e rode `python3 financas/build_data.py`."""
import json, pathlib

# categoria -> (natureza, % que dá para cortar sem mudar de vida)
CATEGORIAS = {
    "Moradia": ("Fixo", 0),
    "Telefone & internet": ("Fixo", 0.40),
    "Assinaturas": ("Fixo", 0),
    "Parcelas": ("Fixo", 0),
    "Outros fixos": ("Fixo", 0),
    "Bares, restaurantes & eventos": ("Variável", 0.30),
    "Delivery": ("Variável", 0.50),
    "Mercado": ("Variável", 0.10),
    "Transporte": ("Variável", 0.30),
    "Compras online": ("Variável", 0.50),
    "Vestuário": ("Variável", 0.30),
    "Viagem": ("Variável", 0),
    "Serviços & avulsos": ("Variável", 0),
    "Cartão Santander": ("Variável", 0),
    "Cartão Itaú não detalhado": ("Variável", 0),
}

OUT_2026 = {
    "mes": "2026-10", "label": "Out 2026", "salario": 16232.00, "fatura_itau": 9370.72,
    "nota": "Contas pagas em outubro. Cartão Itaú: compras de setembro (fatura de vencimento 09/10).",
    "conta": [
        ("Pjbank (boleto, provável aluguel)", 3217.63, "Moradia"),
        ("Condomínio Ed. Paço da Pompeia", 1329.37, "Moradia"),
        ("Enel (luz)", 109.93, "Moradia"),
        ("Comgás (gás)", 12.40, "Moradia"),
        ("TIM", 219.36, "Telefone & internet"),
        ("Claro", 130.34, "Telefone & internet"),
        ("Itaú, boleto avulso (a identificar)", 86.53, "Outros fixos"),
        ("Fatura Santander Unique (sem detalhe)", 243.41, "Cartão Santander"),
    ],
    # (data, descrição, valor, categoria)
    "cartao": [
        ("21/03","Zerezes (parcela 7/8)",174.37,"Parcelas"),
        ("29/07","GOL Linhas Aéreas (parcela 3/3)",521.94,"Parcelas"),
        ("01/09","Uber",14.98,"Transporte"),
        ("01/09","Boracharia MV",1272.00,"Serviços & avulsos"),
        ("01/09","Keeta · PB Boutique",36.99,"Delivery"),
        ("03/09","Keeta · Restaurante Chi",22.49,"Delivery"),
        ("03/09","iFood · Coffee Lab",38.99,"Delivery"),
        ("03/09","Mini Extra",47.14,"Mercado"),
        ("04/09","Itaquaquecetuba (estrada)",6.10,"Viagem"),
        ("04/09","Rafael Augusto (Itaquá)",15.89,"Viagem"),
        ("04/09","Restaurante Galeria (Paraty)",160.38,"Viagem"),
        ("04/09","PHD Paraty",32.99,"Viagem"),
        ("04/09","Destilaria Paratiana",49.90,"Viagem"),
        ("05/09","Bartholomeu Primitivo (Paraty)",208.80,"Viagem"),
        ("05/09","Moradores de Trindade",30.00,"Viagem"),
        ("05/09","Lucas Inácio (Paraty)",154.92,"Viagem"),
        ("06/09","Drogaria (Paraty)",57.40,"Viagem"),
        ("06/09","Carneiro Santos (Paraty)",78.00,"Viagem"),
        ("06/09","Mercado Livre",119.49,"Compras online"),
        ("06/09","Mercado Livre · Celiabordi",123.40,"Compras online"),
        ("06/09","Mercado Livre · Flex",85.98,"Compras online"),
        ("06/09","Mercado Livre",159.90,"Compras online"),
        ("07/09","Balanceia Lounge Bar (Paraty)",306.60,"Viagem"),
        ("07/09","Apple.com/bill",34.90,"Assinaturas"),
        ("07/09","Bar e Restaurante Cent (Paraty)",34.90,"Viagem"),
        ("08/09","Quinta Brasilis Hotel (Paraty)",109.00,"Viagem"),
        ("08/09","Padoca (Paraty)",28.00,"Viagem"),
        ("08/09","Restaurante Piemonte (Caçapava)",20.00,"Viagem"),
        ("08/09","Mini Extra",44.09,"Mercado"),
        ("09/09","Keeta · PB Boutique",46.74,"Delivery"),
        ("09/09","Mercado Livre",90.99,"Compras online"),
        ("09/09","Mercado Livre",106.42,"Compras online"),
        ("09/09","Mahoe Alimentos",28.00,"Mercado"),
        ("09/09","Ki Garapa",12.00,"Mercado"),
        ("09/09","Giani Frutas",32.00,"Mercado"),
        ("09/09","Barraca do Bene",6.00,"Bares, restaurantes & eventos"),
        ("09/09","MP · Yagodonizete",10.00,"Serviços & avulsos"),
        ("09/09","MP · Tapiocederos",42.00,"Bares, restaurantes & eventos"),
        ("09/09","Vitor",41.00,"Serviços & avulsos"),
        ("09/09","Forno Fecchio Padaria",35.20,"Mercado"),
        ("10/09","Mercado Livre",90.61,"Compras online"),
        ("10/09","Keeta · Sushi CWC",27.61,"Delivery"),
        ("10/09","Rappi · Moustache Beams",147.61,"Mercado"),
        ("11/09","Administradora Guarulhos",31.00,"Transporte"),
        ("11/09","Administradora Guarulhos",31.00,"Transporte"),
        ("12/09","Esquina do Souza",201.25,"Bares, restaurantes & eventos"),
        ("12/09","iFood",12.90,"Delivery"),
        ("12/09","Rappi · Moustache Beams",178.01,"Mercado"),
        ("12/09","Uber",55.30,"Transporte"),
        ("12/09","ZigPay",253.89,"Bares, restaurantes & eventos"),
        ("12/09","Tu És Pão",65.00,"Mercado"),
        ("12/09","Zig · Coala 2026",50.00,"Bares, restaurantes & eventos"),
        ("12/09","Zig · Coala 2026",40.00,"Bares, restaurantes & eventos"),
        ("13/09","iFood · Galeto di Paolo",134.34,"Delivery"),
        ("13/09","NetPark",50.00,"Transporte"),
        ("13/09","Mag Bistrô",15.00,"Bares, restaurantes & eventos"),
        ("13/09","Mag Bistrô",30.00,"Bares, restaurantes & eventos"),
        ("14/09","Lanches Pé Pra Fora",25.19,"Bares, restaurantes & eventos"),
        ("14/09","Uber",21.98,"Transporte"),
        ("14/09","Mercado Livre",91.91,"Compras online"),
        ("15/09","iFood · Papila",40.67,"Delivery"),
        ("15/09","Uber",29.44,"Transporte"),
        ("15/09","Rappi · Moustache Beams",149.94,"Mercado"),
        ("16/09","Mahoe Alimentos",28.00,"Mercado"),
        ("16/09","Ki Garapa",13.00,"Mercado"),
        ("17/09","Uber",37.98,"Transporte"),
        ("17/09","Uber",20.97,"Transporte"),
        ("17/09","Uber",38.97,"Transporte"),
        ("17/09","iFood · Blue Deli",72.68,"Delivery"),
        ("18/09","Apple.com/bill",19.90,"Assinaturas"),
        ("19/09","Fukuya Kanemoto",21.99,"Mercado"),
        ("19/09","Lojas Mel Faria",74.97,"Vestuário"),
        ("19/09","Yidstudio Café",38.00,"Bares, restaurantes & eventos"),
        ("19/09","Adega Habibi",241.88,"Bares, restaurantes & eventos"),
        ("20/09","Mercado Livre",97.63,"Compras online"),
        ("20/09","Restaurante Caiçara (Santos)",167.28,"Bares, restaurantes & eventos"),
        ("21/09","Mercado Livre",20.00,"Compras online"),
        ("21/09","Google",4.50,"Assinaturas"),
        ("21/09","Alielton Ribeiro",27.05,"Bares, restaurantes & eventos"),
        ("21/09","iFood · Papila",49.89,"Delivery"),
        ("22/09","Auto Posto Reivilo",18.99,"Transporte"),
        ("22/09","Auto Posto Reivilo",14.99,"Transporte"),
        ("22/09","Auto Posto Reivilo",100.00,"Transporte"),
        ("23/09","Uber",5.96,"Transporte"),
        ("23/09","Floreado Restaurante",97.44,"Bares, restaurantes & eventos"),
        ("23/09","iFood · Casa Buzina",47.74,"Delivery"),
        ("24/09","Taxa de entrega de visto",69.00,"Serviços & avulsos"),
        ("24/09","Rappi · Moustache Beams",129.14,"Mercado"),
        ("24/09","Wellhub",149.99,"Assinaturas"),
        ("24/09","MP · Lisatelier",15.00,"Serviços & avulsos"),
        ("24/09","Uber",32.98,"Transporte"),
        ("25/09","iFood",112.78,"Delivery"),
        ("26/09","Uber",21.45,"Transporte"),
        ("27/09","IPO Bar",182.89,"Bares, restaurantes & eventos"),
        ("27/09","Uber",21.98,"Transporte"),
        ("27/09","Jim.com",100.00,"Serviços & avulsos"),
        ("27/09","Tutoia",150.00,"Serviços & avulsos"),
        ("27/09","ZigPay",10.50,"Bares, restaurantes & eventos"),
        ("27/09","Pop Up Pinheiros",119.99,"Vestuário"),
        ("27/09","ZigPay",20.00,"Bares, restaurantes & eventos"),
        ("27/09","iFood",72.99,"Delivery"),
        ("28/09","Rappi · Moustache Beams",96.65,"Mercado"),
        ("28/09","Uber",14.98,"Transporte"),
        ("28/09","São Cristóvão",81.00,"Bares, restaurantes & eventos"),
        ("28/09","Pátio Café",11.00,"Bares, restaurantes & eventos"),
        ("30/09","iFood · Dona Deola",30.92,"Delivery"),
    ],
}

MESES = [OUT_2026]

def build():
    lanc, meses = [], []
    for m in MESES:
        n = 0
        def add(data, desc, valor, cat, origem):
            nonlocal n
            n += 1
            nat, corte = CATEGORIAS[cat]
            lanc.append({"id": f"{m['mes']}-{n:03d}", "mes": m["mes"], "data": data, "descricao": desc,
                         "valor": round(valor, 2), "categoria": cat, "natureza": nat,
                         "origem": origem, "corte_pct": corte})
        for desc, v, cat in m["conta"]:
            add("", desc, v, cat, "Conta corrente")
        soma = 0.0
        for d, desc, v, cat in m["cartao"]:
            add(d, desc, v, cat, "Cartão Itaú"); soma += v
        resto = round(m["fatura_itau"] - soma, 2)
        if resto > 0.005:
            add("", "Itens da fatura Itaú não enviados (diferença para o total)", resto,
                "Cartão Itaú não detalhado", "Cartão Itaú")
        meses.append({"mes": m["mes"], "label": m["label"], "salario": m["salario"], "nota": m["nota"]})
        print(m["mes"], "cartão listado", round(soma, 2), "fatura", m["fatura_itau"], "diferença", resto)
    out = pathlib.Path(__file__).with_name
    out("lancamentos.json").write_text(json.dumps(lanc, ensure_ascii=False, indent=1))
    out("meses.json").write_text(json.dumps(meses, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    build()
