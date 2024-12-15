# Base62 karakter seti
BASE62_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

def to_base62(num):
    """Bir sayıyı Base62 formatına çevirir."""
    if num == 0:
        return BASE62_CHARS[0]
    
    result = ""
    base = len(BASE62_CHARS)
    
    while num > 0:
        result = BASE62_CHARS[num % base] + result
        num //= base
    
    return result

def base62_batch(start, end):
    """Belirli bir aralıktaki tüm sayıları Base62'ye çevirir."""
    return {i: to_base62(i) for i in range(start, end + 1)}

# Örnek kullanım
number = int(input("Enter a number: "))
converted = to_base62(number)
print(f"Number: {number}, Base62: {converted}")


