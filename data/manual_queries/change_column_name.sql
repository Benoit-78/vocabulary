
ALTER TABLE version_voc CHANGE russian `foreign` CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE version_voc CHANGE français `native` CHAR(255);
ALTER TABLE theme_voc CHANGE russian `foreign` CHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE theme_voc CHANGE français `native` CHAR(255);