# Instagram Username Checker


**برنامج يتحقق من توفر اسم المستخدم على إنستقرام.**  
يعتمد على استخدام قائمة من البروكسيات لتجنب الحظر أو المشاكل المحتملة أثناء عملية الفحص.

### المتطلبات
- **بايثون 3**
- مكتبات: `requests` و `tkinter` (قد تكون مثبتة مسبقًا في معظم التوزيعات)
- ملف نصي يحتوي على أسماء المستخدمين (كل اسم في سطر)
- ملف نصي يحتوي على بروكسيات تدعم HTTPS (كل بروكسي في سطر)

### طريقة الاستخدام
1. اضغط على **Load Usernames** لاختيار الملف الذي يحتوي على أسماء المستخدمين.
2. اضغط على **Load Proxies** لاختيار الملف الذي يحتوي على البروكسيات.
3. قم بضبط عدد الخيوط (**Threads**)، فترة التأخير بين الطلبات (**Delay**)، وعدد المحاولات القصوى (**Max Retries**) حسب الرغبة.
4. اضغط على **Start** لبدء عملية الفحص.
5. عند الانتهاء، يمكنك حفظ قائمة الأسماء المتاحة بالضغط على **Save Lists**.

### ملاحظات مهمة
- يُنصح باستخدام بروكسيات موثوقة وعالية الجودة، لأن البروكسيات الضعيفة قد تؤدي إلى أخطاء في الاتصال.
- السكربت يستخدم لستة البروكسيات IP:Port أو  IP:PORT:USER:PASS.
- إذا تم حظر بروكسي معين أو فشل في الاتصال، سيحاول البرنامج استخدام بروكسي آخر أو إعادة المحاولة حتى الوصول للحد الأقصى من المحاولات.
- هذا السكربت قديم وربما يتم تحديثه في المستقبل لإضافة ميزات أو تحسين الأداء.

### الغرض
هذا البرنامج مخصص لأغراض **التعليم** فقط، وتقع المسؤولية الكاملة على المستخدم في كيفية استعماله.

---

## English

**A program that checks the availability of Instagram usernames.**  
It uses a list of proxies to avoid bans or other issues during the checking process.

### Requirements
- **Python 3**
- Libraries: `requests` and `tkinter` (usually included by default on many systems)
- A text file with usernames (one per line)
- A text file with proxies supporting HTTPS (one per line)

### How to Use
1. Click **Load Usernames** to select the file containing the usernames.
2. Click **Load Proxies** to select the file containing the proxies.
3. Configure **Threads**, **Delay**, and **Max Retries** as desired.
4. Click **Start** to begin the checking process.
5. Once the process finishes, click **Save Lists** to save the list of available usernames.

### Important Notes
- It is recommended to use high-quality, reliable proxies. Weak proxies may cause connection errors.
The script can use a proxy list in the format IP:Port or IP:Port:User:Pass.
- If a specific proxy is blocked or fails to connect, the program will switch to another proxy or retry until the maximum retries limit is reached.
- Note: This script is old and may be updated in the future to add new features or improve performance.


### Purpose
WARNING ! This program is for **educational** purposes only. The user is solely responsible for any use. 





"# Instagram-Checker" 
