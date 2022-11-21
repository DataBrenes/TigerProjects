COPY breakdown_dashboard FROM 'database/breakdown_dashboard.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
COPY cfrm FROM 'database/cfrm.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
COPY gw_res FROM 'database/gw_res.csv' (FORMAT 'csv', quote '"', delimiter ',', header 0);
