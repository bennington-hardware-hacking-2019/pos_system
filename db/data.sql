/* pre-populated data */

INSERT INTO "buyer" VALUES (DEFAULT, 28640, 10000, 'hoanh', 'hoanhan@bennington.edu');

INSERT INTO "admin" VALUES (DEFAULT, 28640, TRUE);

INSERT INTO "item" VALUES (DEFAULT, '{100,0,0}', 'sample item 1', 'sample description 1',  1.11, DEFAULT, NULL);
INSERT INTO "item" VALUES (DEFAULT, '{200,0,0}', 'sample item 2', 'sample description 2',  2.22, DEFAULT, NULL);
INSERT INTO "item" VALUES (DEFAULT, '{300,0,0}', 'sample item 3', 'sample description 3',  3.33, DEFAULT, NULL);
INSERT INTO "item" VALUES (DEFAULT, '{400,0,0}', 'sample item 4', 'sample description 4',  4.44, DEFAULT, NULL);
INSERT INTO "item" VALUES (DEFAULT, '{500,0,0}', 'sample item 5', 'sample description 5',  5.55, DEFAULT, NULL);

INSERT INTO "stock" VALUES (DEFAULT, 1);
INSERT INTO "stock" VALUES (DEFAULT, 3);
INSERT INTO "stock" VALUES (DEFAULT, 5);
