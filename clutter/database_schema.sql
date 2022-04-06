img
CREAT TABLE img_info(
    img_id int(10) unsigned NOT NULL AUTO_INCREMENT ,
    img_name varchar(50) DEFAULT NULL ,
    img_content varchar(255) DEFAULT NULL ,
    img_category int(10)  DEFAULT NULL ,
    img_attributes varchar(100) DEFAULT NULL,
    PRIMARY KEY (img_id)
)

CREAT TABLE img_hanger_bind(
    bind_id int(10) unsigned NOT NULL AUTO_INCREMENT ,
    is_bind int(10) unsigned NOT NULL,
    img_id int(10) unsigned,
    hanger_id int(10) unsigned ,
    img_name varchar(50) DEFAULT NULL ,
    PRIMARY KEY (img_id),
    FOREIGN KEY (hanger_id) REFERENCES hanger_status(hanger_id)
    FOREIGN KEY (img_id) REFERENCES img_info(img_id)
)

CREAT TABLE hanger_status(
    hanger_id int(10) unsigned NOT NULL AUTO_INCREMENT ,
    hanger_address varchar(50) DEFAULT NULL,
    is_bind int(10) unsigned NOT NULL,
    hanger_status int(10) NOT NULL ,
    PRIMARY KEY (hanger_id)
)




