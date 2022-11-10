# Base requirements
As we continue to modulize and simplify the scraper process these are some of the common requirements. 
## Selenium chrome docket image 
```
docker run -d -p 4444:4444 -p 7900:7900 --name selenium4 --shm-size="2g" selenium/standalone-chrome:4.4.0-20220831
```