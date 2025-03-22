from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import random
import os

def sozlugu_yukle():
    sozluk = {}
    if os.path.exists("sozluk.txt"):
        with open("sozluk.txt", "r", encoding="utf-8") as f:
            for satir in f:
                try:
                    kelime, anlam = satir.strip().split(":")
                    sozluk[kelime] = anlam
                except ValueError:
                    continue
    return sozluk

def sozlugu_kaydet():
    with open("sozluk.txt", "w", encoding="utf-8") as f:
        for kelime, anlam in sozluk.items():
            f.write(f"{kelime}:{anlam}\n")

sozluk = sozlugu_yukle()
ters_sozluk = {v: k for k, v in sozluk.items()}

class MainScreen(Screen):
    pass

class DictionaryScreen(Screen):
    def kelime_ara(self):
        kelime = self.ids.entry.text.capitalize()
        anlam = sozluk.get(kelime, ters_sozluk.get(kelime, "Bu kelime sözlükte bulunmamaktadır."))
        self.ids.result_label.text = f"{kelime} -> {anlam}"

    def kelime_ekle(self):
        yeni_kelime = self.ids.new_word.text.capitalize()
        yeni_anlam = self.ids.new_meaning.text.capitalize()
        if yeni_kelime and yeni_anlam:
            sozluk[yeni_kelime] = yeni_anlam
            sozlugu_kaydet()
            self.ids.new_word.text = ""
            self.ids.new_meaning.text = ""
            self.ids.result_label.text = f"✅ '{yeni_kelime}' eklendi!"

    def kelime_sil(self):
        sil_kelime = self.ids.delete_word.text.capitalize()
        if sil_kelime in sozluk:
            del sozluk[sil_kelime]
            sozlugu_kaydet()
            self.ids.delete_word.text = ""
            self.ids.result_label.text = f"❌ '{sil_kelime}' silindi!"
        else:
            self.ids.result_label.text = "⚠️ Kelime bulunamadı!"

class QuizScreen(Screen):
    def yeni_soru(self):
        if random.choice([True, False]):
            self.soru_tipi = "ing-tr"
            self.quiz_kelime, self.quiz_cevap = random.choice(list(sozluk.items()))
        else:
            self.soru_tipi = "tr-ing"
            self.quiz_kelime, self.quiz_cevap = random.choice(list(ters_sozluk.items()))

        self.ids.quiz_label.text = f"❓ {self.quiz_kelime} ne anlama gelir?"
        self.ids.quiz_result.text = ""

        secenekler = random.sample(list(sozluk.values() if self.soru_tipi == "ing-tr" else ters_sozluk.values()), 3)
        if self.quiz_cevap not in secenekler:
            secenekler[random.randint(0, 2)] = self.quiz_cevap
        random.shuffle(secenekler)

        for i, secenek in enumerate(secenekler):
            self.ids[f"option_{i+1}"].text = secenek

    def kontrol_et(self, cevap):
        if cevap == self.quiz_cevap:
            self.ids.quiz_result.text = "✅ Doğru!"
        else:
            self.ids.quiz_result.text = f"❌ Yanlış! Doğru cevap: {self.quiz_cevap}"

class SozlukApp(App):
    def build(self):
        Builder.load_file("mobil_sozluk.kv")
        sm = ScreenManager()

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(DictionaryScreen(name='dictionary'))
        sm.add_widget(QuizScreen(name='quiz'))

        sm.current = 'main'  # <- açılış ekranı sorunu çözülür
        return sm

if __name__ == '__main__':
    SozlukApp().run()
