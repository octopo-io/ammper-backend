CREATE TABLE user_links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    link_id VARCHAR(255) not null,
    institution VARCHAR(255) not null,
    FOREIGN KEY (user_id) REFERENCES users(id)
);