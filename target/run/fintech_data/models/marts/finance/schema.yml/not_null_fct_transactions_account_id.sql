select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select account_id
from "neondb"."public"."fct_transactions"
where account_id is null



      
    ) dbt_internal_test