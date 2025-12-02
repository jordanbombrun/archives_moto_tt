-- schema of the DB in schema.sql
INSERT OR IGNORE INTO category (name)
VALUES ('black'), ('red'), ('green'), ('blue'), ('pink'), ('or'), ('argent'), ('bronze'),('elite'), ('junior'), ('espoir'), ('veteran'), ('super veteran'), ('feminin'), ('open'), ('nationale'), ('nationale E1'), ('nationale E2'), ('nationale E3'), ('regionale'), ('regionale E1'), ('regionale E2'), ('regionale E3'), ('solo'), ('duo');

INSERT OR IGNORE INTO serie (name, year)
VALUES ('Extrême challenge', 2025), ('Ligue Aura enduro', 2025), ('Ligue Aura endurance', 2025), ('Championnat de France enduro', 2025), ('Championnat de France motocross', 2025), ('Championnat de France Cross Country', 2025); 

INSERT OR IGNORE INTO format (name)
VALUES ('Enduro'), ('Cross country'), ('Endurance'), ('Enduro extrême'), ('Motocross'), ('Supercross'), ('Enduro sprint'), ('Rallye'), ('Super enduro');
