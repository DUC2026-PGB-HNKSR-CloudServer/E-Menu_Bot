# 🍔 E-Menu Telegram Bot (ប្រព័ន្ធកុម្ម៉ង់អាហារឌីជីថល)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Telebot](https://img.shields.io/badge/Telebot-pyTelegramBotAPI-green)
![Supabase](https://img.shields.io/badge/Database-Supabase-black)

**E-Menu Bot** គឺជាប្រព័ន្ធកុម្ម៉ង់អាហារឆ្លាតវៃតាមរយៈ Telegram ដែលត្រូវបានបង្កើតឡើងដើម្បីជួយសម្រួលដល់ភោជនីយដ្ឋាន ឬហាងកាហ្វេ ក្នុងការទទួលការកុម្ម៉ង់ពីភ្ញៀវ (Dine-in) បានយ៉ាងលឿន និងមានប្រសិទ្ធភាព។ អតិថិជនគ្រាន់តែស្កេន QR Code នៅលើតុ នោះ Bot នឹងបើកម៉ឺនុយឱ្យកុម្ម៉ង់ភ្លាមៗ!

## ✨ លក្ខណៈពិសេសចម្បង (Key Features)

* **🌐 ប្រព័ន្ធ ២ ភាសា (Bilingual):** គាំទ្រទាំងភាសាខ្មែរ និងអង់គ្លេស។
* **☁️ Dynamic Menu:** បញ្ជីមុខម្ហូប និងតម្លៃត្រូវបានទាញចេញពី Database ផ្ទាល់ (ងាយស្រួលកែប្រែដោយមិនបាច់ប៉ះពាល់កូដ)។
* **🛒 ប្រព័ន្ធកន្ត្រក (Cart System):** អតិថិជនអាចជ្រើសរើសមុខម្ហូប និងកំណត់ចំនួន មុននឹងបញ្ជាទិញ។
* **👨‍🍳 ផ្ទាំងគ្រប់គ្រង Admin (In-chat Dashboard):** Admin ទទួលបានសារដំណឹងពេលមានការកុម្ម៉ង់ថ្មី ហើយអាចចុចប៊ូតុង "ទទួលយក", "បដិសេធ" ឬ "កំពុងយកទៅតុ" ពីក្នុង Telegram ផ្ទាល់។
* **🛎 សេវាកម្មតុ (Table Services):** ភ្ញៀវអាចហៅអ្នករត់តុ សុំទឹកកក សុំក្រដាស ឬសុំគិតលុយ តាមរយៈប៊ូតុង។
* **📊 របាយការណ៍លក់ប្រចាំថ្ងៃ:** Admin អាចឆែកមើលចំនួនលក់ និងចំណូលសរុបប្រចាំថ្ងៃបានតាមរយៈពាក្យបញ្ជា។

* 📱 ពាក្យបញ្ជា (Commands)
* /start - បើកដំណើរការ Bot និងជ្រើសរើសភាសា (ភ្ញៀវទូទៅ)
* /broadcast - ផ្ញើសារប្រូម៉ូសិនទៅកាន់អតិថិជនទាំងអស់ (សម្រាប់តែ Admin)
* /report - មើលរបាយការណ៍ចំណូល និងមុខម្ហូបលក់ដាច់ប្រចាំថ្ងៃ (សម្រាប់តែ Admin)

## 🛠 បច្ចេកវិទ្យាដែលប្រើប្រាស់ (Tech Stack)
* **ភាសាសរសេរកូដ:** Python 3
* **បណ្ណាល័យ Bot:** `pyTelegramBotAPI`
* **មូលដ្ឋានទិន្នន័យ (Database):** Supabase (PostgreSQL)

## 🚀 របៀបដំឡើង និងដាក់ឱ្យដំណើរការ (Installation & Setup)

**១. ទាញយកគម្រោងនេះ (Clone the repo)**
```bash
git clone [https://github.com/DUC2026-PGB-HNKSR-CloudServer/emenu-bot.git](https://github.com/DUC2026-PGB-HNKSR-CloudServer/emenu-bot.git)
cd emenu-bot

