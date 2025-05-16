# 小テスト flask app
## Summary
USMLE Step1の小テストを出題するアプリケーションです。
https://medical-quizholic-777033964912.asia-northeast1.run.app

## 使用技術
- Front end
  - HTML, CSS, Bootstrap5
  - Javascript
- Back end
  - Library: Python Flask, SQLAlchemy
  - DB: MySQL
  - Infrastructure: Google Cloud(Cloud run, Cloud SQL)
  - Authentication: Google OAuth2, DB認証, Guest user

## DB schema
### Users table
```
`users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(512) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `latest_login` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `auth_provider` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) 
```
E-mailで一意性を担保。

### Questions table
```
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` text,
  `choices` json NOT NULL,
  `correct_answer` int NOT NULL,
  `explanation` text,
  `image_path` varchar(255) DEFAULT NULL,
  `section_id` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ix_questions_section_id` (`section_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `sections` (`section_id`)
)
```

### Sections table
```
CREATE TABLE `sections` (
  `section_id` int NOT NULL AUTO_INCREMENT,
  `section_name` varchar(100) NOT NULL,
  `unit` varchar(100) NOT NULL,
  `chapter` varchar(100) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`section_id`),
  UNIQUE KEY `section_name` (`section_name`)
)
```
Category > Chapter > Unit > Section

例)
> Microbiology > Bacteria > Gram positive cocci > Staphylococcus aureus

## Todo
- [ ] 非同期通信の実装
- [ ] Userごとの正答率履歴・解答履歴の表示。
