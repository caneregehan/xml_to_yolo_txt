import os
import xml.etree.ElementTree as ET

# XML dosyalarının bulunduğu dizin
xml_dir = "your_path"

# Çıktı dosyalarının bulunacağı dizin
output_dir = "output_path"

# Sınıf etiketleri
class_labels = {"RBC": 0, "WBC": 1, "Platelet": 2, "Thalasemia": 3}

# XML dosyalarını işleme döngüsü
for filename in os.listdir(xml_dir):
    if filename.endswith(".xml"):
        # XML dosyasının tam yolu
        xml_file = os.path.join(xml_dir, filename)
        
        # Çıktı dosyasının adını oluştur
        output_file = os.path.splitext(filename)[0] + ".txt"
        output_file = os.path.join(output_dir, output_file)
        
        # XML dosyasını açma ve içeriğini okuma
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # .txt dosyasını açma ve içine yazma
        with open(output_file, "w") as f:
            # Her bir nesne etiketi için döngü
            for obj in root.findall(".//object"):
                # Nesne adını al
                name = obj.find("name").text
                
                # Koordinatları al
                bbox = obj.find("bndbox")
                xmin = int(bbox.find("xmin").text)
                ymin = int(bbox.find("ymin").text)
                xmax = int(bbox.find("xmax").text)
                ymax = int(bbox.find("ymax").text)
                
                # YOLO formatına dönüştürme
                img_width = int(root.find(".//size/width").text)
                img_height = int(root.find(".//size/height").text)
                x_center = (xmin + xmax) / 2 / img_width
                y_center = (ymin + ymax) / 2 / img_height
                width = (xmax - xmin) / img_width
                height = (ymax - ymin) / img_height
                
                # Etiket değerini belirle
                label = class_labels.get(name)
                
                # Yazma işlemi
                if label is not None:
                    f.write(f"{label} {x_center} {y_center} {width} {height}\n")

