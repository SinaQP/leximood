from src.leximood.analyzer import analyze_text
import datetime


def test_sentiment_analysis():
    """تست تحلیل احساسات با جملات مختلف فارسی"""
    
    test_sentences = [
        # جملات مثبت
        "من عاشق این محصول هستم و میخوام بیشتر از این محصول بخرم",
        "این رستوران فوق‌العاده است و غذاهایش خیلی خوشمزه هستند",
        "امروز روز بسیار خوبی بود و خوشحالم",
        "این فیلم واقعاً عالی بود و حتماً دوباره می‌بینم",
        "دوستت دارم و خوشحالم که با تو آشنا شدم",
        
        # جملات منفی
        "این محصول افتضاح است و پولم را هدر دادم",
        "امروز روز بدی بود و ناراحتم",
        "این غذا خیلی بد بود و اصلاً خوشمزه نبود",
        "از این فیلم متنفرم و وقتم را تلف کردم",
        "خیلی عصبانی هستم و نمی‌خوام کسی را ببینم",
        
        # جملات خنثی
        "امروز هوا ابری است",
        "این کتاب ۲۰۰ صفحه دارد",
        "ساعت ۳ بعدازظهر است",
        "این ماشین قرمز رنگ است",
        "فردا روز دوشنبه است",
        
        # جملات ترکیبی (مثبت و منفی)
        "این محصول خوب است اما قیمتش خیلی گران است",
        "فیلم جالبی بود اما خیلی طولانی بود",
        "رستوران تمیز بود اما غذا خیلی دیر آمد",
        "هوا خوب است اما ترافیک وحشتناک است",
        "کتاب مفیدی بود اما خیلی سخت بود"
    ]
    
    # آماده کردن محتوای فایل
    output_lines = []
    output_lines.append("=" * 60)
    output_lines.append("تست تحلیل احساسات LexiMood")
    output_lines.append(f"تاریخ و زمان: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output_lines.append("=" * 60)
    
    for i, sentence in enumerate(test_sentences, 1):
        try:
            result = analyze_text(sentence)
            output_lines.append(f"\n{i:2d}. جمله: {sentence}")
            output_lines.append(f"    احساس: {result.sentiment.value}")
            output_lines.append(f"    امتیاز: {result.score:.3f}")
            output_lines.append(f"    اطمینان: {result.confidence:.3f}")
            if result.keywords:
                output_lines.append(f"    کلمات کلیدی: {', '.join(result.keywords)}")
        except Exception as e:
            output_lines.append(f"\n{i:2d}. خطا در تحلیل: {e}")
    
    output_lines.append("\n" + "=" * 60)
    output_lines.append("پایان تست")
    
    # ذخیره در فایل
    with open("sentiment_test_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    # نمایش در کنسول
    print("\n".join(output_lines))
    print(f"\nنتایج در فایل 'sentiment_test_results.txt' ذخیره شد.")


if __name__ == "__main__":
    test_sentiment_analysis()