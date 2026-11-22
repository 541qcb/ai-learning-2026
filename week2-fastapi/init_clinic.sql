SET NAMES utf8mb4;
CREATE TABLE IF NOT EXISTS patients (
  patient_id VARCHAR(10) PRIMARY KEY,
  name       VARCHAR(50) NOT NULL,
  dept       VARCHAR(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS visits (
  visit_id   INT AUTO_INCREMENT PRIMARY KEY,
  patient_id VARCHAR(10) NOT NULL,
  visit_date DATE NOT NULL,
  total_fee  DOUBLE NOT NULL,
  diagnosis  VARCHAR(100),
  INDEX idx_patient (patient_id),
  INDEX idx_date (visit_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO patients VALUES
('P001','张三','内科'),('P002','李四','外科'),('P003','王五','儿科'),
('P004','张丽','神经内科'),('P005','张可','神经外科'),('P006','张忍','呼吸内科'),
('P007','赵六','眼科'),('P008','孙六','骨科'),('P009','周八','皮肤科'),('P010','钱七','急诊科');

INSERT INTO visits (patient_id, visit_date, total_fee, diagnosis) VALUES
('P001','2026-10-02', 235.5,'上呼吸道感染'),
('P001','2026-10-09',1500.0,'高血压'),
('P001','2026-10-16', 160.0,'复查'),
('P001','2026-10-23',2080.0,'糖尿病'),
('P002','2026-10-05', 880.0,'阑尾炎'),
('P003','2026-10-06', 456.7,'肺炎'),
('P004','2026-10-11',1200.0,'脑梗死'),
('P005','2026-10-14',3200.0,'脑膜瘤'),
('P006','2026-10-18', 990.0,'慢阻肺'),
('P007','2026-10-19', 300.0,'结膜炎');
