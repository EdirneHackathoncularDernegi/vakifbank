from flask import Flask, render_template, request, jsonify, redirect, url_for
import json

app = Flask(__name__)
@app.context_processor
def utility_processor():
    return dict(enumerate=enumerate)
faktorler = {
            "Dışadönüklük": {
                "sorular": [
                    "İnsanlarla konuşmayı severim.",
                    "Kalabalık gruplarda kendimi rahat hissederim.",
                    "Çevremdekilere enerji veren bir yapım vardır.",
                    "Eğlenceli ve keyifli biri olarak tanınırım.",
                    "Sosyal etkinliklere katılmayı tercih ederim.",
                    "Yeni insanlarla tanışmayı kolay bulurum.",
                    "Yalnız kalmayı tercih ederim.",  # Ters
                    "İletişim kurarken kendimi ifade etmekte zorlanırım.",  # Ters
                    "Göz önünde olmaktan hoşlanırım.",
                    "Konuşmalarımı enerjik bir şekilde sürdürürüm."
                ],
                "ters_sorular": [7, 8]
            },
            "Uyumluluk": {
                "sorular": [
                    "İnsanlara yardım etmekten keyif alırım.",
                    "Çoğu zaman başkalarının ihtiyaçlarını kendi ihtiyaçlarımın önüne koyarım.",
                    "İnsanlar beni güvenilir biri olarak görür.",
                    "İş arkadaşlarıma destek vermekten mutluluk duyarım.",
                    "Başkalarının duygularını anlama konusunda iyiyimdir.",
                    "Çatışmalardan kaçınmaya çalışırım.",
                    "Karşımdakine empatiyle yaklaşırım.",
                    "Kendi fikirlerimi savunma konusunda ısrarcıyımdır.",  # Ters
                    "İnsanların ihtiyaçlarını dikkate alırım.",
                    "Beni zorlasa bile işbirliği yaparım."
                ],
                "ters_sorular": [18]
            },
            "Özdenetim": {
                "sorular": [
                    "İşlerimi düzenli bir şekilde yürütürüm.",
                    "Uzun vadeli hedeflerime sadık kalırım.",
                    "Zamanımı iyi yönetebilirim.",
                    "Plan yapmadan çalışmayı tercih ederim.",  # Ters
                    "Sorumluluk almayı severim.",
                    "Görevlerimi zamanında tamamlarım.",
                    "Ertelemeyi alışkanlık haline getiririm.",  # Ters
                    "Çalışma ortamımı organize ederim.",
                    "Disiplinli bir şekilde çalışırım.",
                    "Beklenmedik durumlarda planlarımı değiştirmekte zorlanırım."
                ],
                "ters_sorular": [24, 27]
            },
            "Nörotiklik": {
                "sorular": [
                    "Stresli durumlarda kolayca kaygılanırım.",
                    "Duygusal dalgalanmalar yaşarım.",
                    "Kritik anlarda sakin kalmakta zorlanırım.",
                    "Çabuk sinirlenirim.",
                    "Küçük sorunlar beni strese sokar.",
                    "Belirsizlikten hoşlanmam.",
                    "Zor durumlarla baş etmekte zorlanırım.",
                    "Hayal kırıklığına uğradığımda sakin kalırım.",  # Ters
                    "Kendime güvenim tamdır.",  # Ters
                    "Kaygılı bir yapıya sahibim."
                ],
                "ters_sorular": [38, 39]
            },
            "Deneyime Açıklık": {
                "sorular": [
                    "Yeni fikirleri ve değişiklikleri kucaklarım.",
                    "Farklı kültürlerden insanlar ve gelenekler beni etkiler.",
                    "Sanat, müzik ve edebiyat gibi alanlarda yeniliklere açık biriyimdir.",
                    "Hayal gücümü kullanmayı severim.",
                    "Merak duygum yüksektir.",
                    "Rutin işler beni sıkar.",
                    "Yaratıcı aktivitelerden keyif alırım.",
                    "Farklı bakış açılarını anlamaya çalışırım.",
                    "Yenilikleri hayatıma adapte etmekte zorlanırım.",  # Ters
                    "Teknolojik yenilikleri takip ederim."
                ],
                "ters_sorular": [49]
            }
        }

def ters_puanlama(puan):
    """Ters puanlama yapılacak sorular için 6'dan çıkarılır."""
    return 6 - puan

@app.route('/')
def index():
    return render_template('index.html', faktorler=faktorler)

@app.route('/submit', methods=['POST'])
def submit():
    toplam_puanlar = {}
    raw_data = {}

    for faktor, bilgiler in faktorler.items():
        sorular = bilgiler["sorular"]
        ters_sorular = bilgiler["ters_sorular"]
        puanlar = []
        yanitlar = {}

        for i, soru in enumerate(sorular, 1):
            yanit = int(request.form.get(f"{faktor}_{i}"))
            yanitlar[f"Soru {i}"] = yanit
            if i in ters_sorular:
                yanit = ters_puanlama(yanit)
            puanlar.append(yanit)

        toplam_puanlar[faktor] = sum(puanlar)
        raw_data[faktor] = yanitlar

    # Ham veriyi kaydet
    with open("ham_veriler.json", "w") as file:
        json.dump(raw_data, file, indent=4)

    # Analizleri hesapla ve yeni template'e render et
    yorumlar = detayli_analiz(toplam_puanlar)
    return render_template('analysis.html', yorumlar=yorumlar)

@app.route('/ham_veri')
def ham_veri():
    try:
        with open("ham_veriler.json", "r") as file:
            data = json.load(file)
        return jsonify(data)
    except FileNotFoundError:
        return "Henüz ham veri kaydedilmedi."

@app.route('/analiz')
def analiz():
    try:
        with open("ham_veriler.json", "r") as file:
            raw_data = json.load(file)

        # Toplam puanları yeniden hesapla
        toplam_puanlar = {}
        for faktor, yanitlar in raw_data.items():
            puanlar = []
            ters_sorular = faktorler[faktor]["ters_sorular"]
            for i, yanit in enumerate(yanitlar.values(), 1):
                if i in ters_sorular:
                    yanit = ters_puanlama(yanit)
                puanlar.append(yanit)
            toplam_puanlar[faktor] = sum(puanlar)

        yorumlar = detayli_analiz(toplam_puanlar)
        return render_template('analysis.html', yorumlar=yorumlar)

    except FileNotFoundError:
        return "Henüz ham veri kaydedilmedi."

def detayli_analiz(puanlar):
    yorumlar = {}
    for faktor, puan in puanlar.items():
        if faktor == "Dışadönüklük":
            if puan >= 40:
                yorumlar[faktor] = "Sosyal, konuşkan ve enerjik bir yapınız var. İş ortamında grup projelerine öncülük edebilir, diğer çalışanları motive edebilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde dışadönüksünüz. Sosyal ortamlarda kendinizi rahat hissetseniz de, bireysel çalışmalarda da başarılı olabilirsiniz."
            else:
                yorumlar[faktor] = "Daha içedönük bir yapınız var. Daha sessiz bir çalışma ortamı tercih edebilir ve bireysel projelerde daha üretken olabilirsiniz."
        
        elif faktor == "Uyumluluk":
            if puan >= 40:
                yorumlar[faktor] = "Son derece yardımsever, empati sahibi ve iş birliğine açık bir yapınız var. Çatışma çözümünde etkili olabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde uyumlusunuz. İş birliğine açık olsanız da, bazen kendi fikirlerinizi savunma konusunda kararlı olabilirsiniz."
            else:
                yorumlar[faktor] = "Daha bireysel hareket eden bir yapınız var. İş yerinde çatışma durumlarında bağımsız çalışmayı tercih edebilirsiniz."

        elif faktor == "Özdenetim":
            if puan >= 40:
                yorumlar[faktor] = "Son derece düzenli, planlı ve sorumluluk sahibi bir yapınız var. Zaman yönetimi ve iş takibi konusunda örnek olabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde özdenetim beceriniz var. Genel olarak düzenli çalışsanız da, zaman zaman planlama eksiklikleri yaşayabilirsiniz."
            else:
                yorumlar[faktor] = "Daha plansız ve düzensiz bir yapınız var. Zaman yönetimi ve iş takibi konusunda desteğe ihtiyaç duyabilirsiniz."

        elif faktor == "Nörotiklik":
            if puan >= 40:
                yorumlar[faktor] = "Stres ve duygusal dalgalanmalar konusunda hassas bir yapınız var. Daha sakin kalmayı öğrenmek için stres yönetimi eğitimleri alabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde nörotiklik özellikleri gösteriyorsunuz. Çoğu durumda sakin kalabilseniz de, zorlayıcı durumlarda kendinizi stresli hissedebilirsiniz."
            else:
                yorumlar[faktor] = "Duygusal açıdan dengeli ve sakin bir yapınız var. Zorlayıcı durumlarla başa çıkma konusunda başarılısınız."

        elif faktor == "Deneyime Açıklık":
            if puan >= 40:
                yorumlar[faktor] = "Yaratıcı, yeniliklere açık ve öğrenmeye meraklı bir yapınız var. Farklı projelerde yeni fikirler geliştirebilir ve çeşitlilikten keyif alabilirsiniz."
            elif 30 <= puan < 40:
                yorumlar[faktor] = "Orta düzeyde deneyime açıklığınız var. Yeniliklere açık olsanız da, zaman zaman alışılmış yöntemleri tercih edebilirsiniz."
            else:
                yorumlar[faktor] = "Daha geleneksel bir yapınız var. Yeniliklere adapte olmakta zorlanabilirsiniz, ancak bu sizi derinlemesine uzmanlaşmaya yönlendirebilir."

    return yorumlar

if __name__ == '__main__':
    app.run(debug=True)