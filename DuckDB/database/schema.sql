


CREATE TABLE breakdown_dashboard("Res_ID" BIGINT, "Date" TIMESTAMP, "Per Night" DOUBLE, "Month-Year" VARCHAR, PRIMARY KEY("Res_ID", "Date", "Per Night", "Month-Year"));
CREATE TABLE cfrm("Res_ID" BIGINT PRIMARY KEY, "Status" VARCHAR, "Unit" VARCHAR, "Guest" VARCHAR, "Booked Date" VARCHAR, "Check-In" VARCHAR, "Checkout" VARCHAR, "Nights" BIGINT, "Income" VARCHAR);
CREATE TABLE gw_res("Res_ID" BIGINT PRIMARY KEY, "Status" VARCHAR, "Unit" VARCHAR, "Guest" VARCHAR, "Booked Date" VARCHAR, "Check-In" VARCHAR, "Checkout" VARCHAR, "Nights" BIGINT, "Income" VARCHAR);




