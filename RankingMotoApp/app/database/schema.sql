CREATE TABLE IF NOT EXISTS "race" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR NOT NULL,
	"date" DATE NOT NULL,
	"location" VARCHAR,
	"serie_id" INTEGER,
	"format_id" INTEGER NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("serie_id") REFERENCES "serie"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY ("format_id") REFERENCES "format"("id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
	UNIQUE(name, date)
);

CREATE TABLE IF NOT EXISTS "rider" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "category" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "chrono" (
	"id" INTEGER NOT NULL UNIQUE,
	"participation_id" INTEGER NOT NULL,
	"current_lap" INTEGER,
	"current_sp" INTEGER,
	"current_race" INTEGER,
	"time" REAL NOT NULL DEFAULT 0.0,
	PRIMARY KEY("id"),
	FOREIGN KEY ("participation_id") REFERENCES "participation"("race_id")
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "penalty" (
	"id" INTEGER NOT NULL UNIQUE,
	"participation_id" INTEGER NOT NULL,
	"time" REAL NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY ("participation_id") REFERENCES "participation"("race_id")
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "log_import_data" (
	"id" INTEGER NOT NULL UNIQUE,
	"imported_at" DATETIME NOT NULL,
	"report" VARCHAR NOT NULL,
	"source_url" VARCHAR NOT NULL,
	"source_content" TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "participation" (
	"race_id" INTEGER NOT NULL,
	"rider_id" INTEGER NOT NULL,
	"number" INTEGER NOT NULL,
	"category_id" INTEGER,
	"team_id" INTEGER,
	"final_position" INTEGER,
	"moto" VARCHAR,
	PRIMARY KEY("race_id", "rider_id"),
	FOREIGN KEY ("race_id") REFERENCES "race"("id")
	ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("rider_id") REFERENCES "rider"("id")
	ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("category_id") REFERENCES "category"("id")
	ON UPDATE CASCADE ON DELETE SET NULL,
	FOREIGN KEY ("team_id") REFERENCES "team"("id")
	ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS "team" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR DEFAULT 'inconnu',
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "checkpoint" (
	"id" INTEGER NOT NULL UNIQUE,
	"particpation_id" INTEGER NOT NULL,
	"current_lap" INTEGER,
	"current_cp" INTEGER NOT NULL,
	"time" TIME NOT NULL DEFAULT '00:00:00',
	PRIMARY KEY("id"),
	FOREIGN KEY ("particpation_id") REFERENCES "participation"("race_id")
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "race_category" (
	"race_id" INTEGER NOT NULL,
	"category_id" INTEGER NOT NULL,
	"nb_lap" INTEGER,
	"nb_cp" INTEGER,
	"nb_sp" INTEGER,
	"nb_round" INTEGER,
	PRIMARY KEY("race_id", "category_id"),
	FOREIGN KEY ("race_id") REFERENCES "race"("id")
	ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY ("category_id") REFERENCES "category"("id")
	ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "serie" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" REAL,
	"year" INTEGER,
	PRIMARY KEY("id")
	UNIQUE(name, year)
);

CREATE TABLE IF NOT EXISTS "format" (
	"id" INTEGER NOT NULL UNIQUE,
	"name" VARCHAR NOT NULL UNIQUE,
	PRIMARY KEY("id")	
);
