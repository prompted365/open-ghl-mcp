## Important API Documentation for the Projects and Assessments Tables and the PDF-Storage Bucket.

## We will leverage a middleware service, GHL Oauth2, their v2 API, and the open-ghl-mcp already in this repository to facilitate the submission of addresses by GoHighLevel and/or Assistable.ai agents via tool call and the return of a pdf to the /media endpoint in GoHighLevel as a file, and the public url of said file to a custom field in the contact object in GoHighLevel. 

## These are the related API docs:

see @SUPABASE_TYPES.tsx for the generated types and the rest of the repo handles oAuth2 and Basic mcp with ghl. I believe we still need to add media and custom field support. 

Columns

| Name | Format | Type | Description | 
| ---- | ---- | ---- | ----  |
| id | 

uuid

 | string |  | 
| project_id | 

uuid

 | string |  | 
| group_id | 

uuid

 | string |  | 
| assessment_stage_id | 

uuid

 | string |  | 
| workflow_template_id | 

uuid

 | string |  | 
| supabase_path_root | 

text

 | string |  | 
| rgb_url | 

text

 | string |  | 
| dsm_url | 

text

 | string |  | 
| mask_url | 

text

 | string |  | 
| flux_overlay_url | 

text

 | string |  | 
| flux_composite_gif_url | 

text

 | string |  | 
| monthly_flux_urls | 

text[]

 | array |  | 
| monthly_composite_flux_urls | 

text[]

 | array |  | 
| building_insights | 

jsonb

 | json |  | 
| created_at | 

timestamp with time zone

 | string |  | 
| updated_at | 

timestamp with time zone

 | string |  | 
| version_number | 

integer

 | number |  | 
| optimal_configuration | 

jsonb

 | json |  | 
| status | 

text

 | string |  | 
| input_approx_utility_bill | 

double precision

 | number |  | 
| derived_monthly_bill_for_selected_config | 

double precision

 | number |  | 
| selected_panel_config_index | 

integer

 | number |  | 

## Read rows

[Documentation](https://supabase.com/docs/reference/javascript/select)

To read rows in this table, use the `select` method.

Read all rows
    
    
    let { data: solar_assessments, error } = await supabase
    
      .from('solar_assessments')
    
      .select('*')

Read specific columns
    
    
    let { data: solar_assessments, error } = await supabase
    
      .from('solar_assessments')
    
      .select('some_column,other_column')

Read referenced tables
    
    
    let { data: solar_assessments, error } = await supabase
    
      .from('solar_assessments')
    
      .select(`
    
        some_column,
    
        other_table (
    
          foreign_key
    
        )
    
      `)

With pagination
    
    
    let { data: solar_assessments, error } = await supabase
    
      .from('solar_assessments')
    
      .select('*')
    
      .range(0, 9)

## Filtering

[Documentation](https://supabase.com/docs/reference/javascript/using-filters)

Supabase provides a wide range of filters

With filtering
    
    
    let { data: solar_assessments, error } = await supabase
    
      .from('solar_assessments')
    
      .select("*")
    
    
    
    
      // Filters
    
      .eq('column', 'Equal to')
    
      .gt('column', 'Greater than')
    
      .lt('column', 'Less than')
    
      .gte('column', 'Greater than or equal to')
    
      .lte('column', 'Less than or equal to')
    
      .like('column', '%CaseSensitive%')
    
      .ilike('column', '%CaseInsensitive%')
    
      .is('column', null)
    
      .in('column', ['Array', 'Values'])
    
      .neq('column', 'Not equal to')
    
    
    
    
      // Arrays
    
      .contains('array_column', ['array', 'contains'])
    
      .containedBy('array_column', ['contained', 'by'])
    
    
    
    
      // Logical operators
    
      .not('column', 'like', 'Negate filter')
    
      .or('some_column.eq.Some value, other_column.eq.Other value')

## Insert rows

[Documentation](https://supabase.com/docs/reference/javascript/insert)

`insert` lets you insert into your tables. You can also insert in bulk and do UPSERT.

`insert` will also return the replaced values for UPSERT.

Insert a row
    
    
    const { data, error } = await supabase
    
      .from('solar_assessments')
    
      .insert([
    
        { some_column: 'someValue', other_column: 'otherValue' },
    
      ])
    
      .select()

Insert many rows
    
    
    const { data, error } = await supabase
    
      .from('solar_assessments')
    
      .insert([
    
        { some_column: 'someValue' },
    
        { some_column: 'otherValue' },
    
      ])
    
      .select()

Upsert matching rows
    
    
    const { data, error } = await supabase
    
      .from('solar_assessments')
    
      .upsert({ some_column: 'someValue' })
    
      .select()

## Update rows

[Documentation](https://supabase.com/docs/reference/javascript/update)

`update` lets you update rows. `update` will match all rows by default. You can update specific rows using horizontal filters, e.g. `eq`, `lt`, and `is`.

`update` will also return the replaced values for UPDATE.

Update matching rows
    
    
    const { data, error } = await supabase
    
      .from('solar_assessments')
    
      .update({ other_column: 'otherValue' })
    
      .eq('some_column', 'someValue')
    
      .select()

## Delete rows

[Documentation](https://supabase.com/docs/reference/javascript/delete)

`delete` lets you delete rows. `delete` will match all rows by default, so remember to specify your filters!

Delete matching rows
    
    
    const { error } = await supabase
    
      .from('solar_assessments')
    
      .delete()
    
      .eq('some_column', 'someValue')

## Subscribe to changes

[Documentation](https://supabase.com/docs/reference/javascript/subscribe)

Supabase provides realtime functionality and broadcasts database changes to authorized users depending on Row Level Security (RLS) policies.

Subscribe to all events
    
    
    const channels = supabase.channel('custom-all-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: '*', schema: 'public', table: 'solar_assessments' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to inserts
    
    
    const channels = supabase.channel('custom-insert-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: 'INSERT', schema: 'public', table: 'solar_assessments' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to updates
    
    
    const channels = supabase.channel('custom-update-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: 'UPDATE', schema: 'public', table: 'solar_assessments' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Copy

Subscribe to deletes
    
    
    const channels = supabase.channel('custom-delete-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: 'DELETE', schema: 'public', table: 'solar_assessments' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to specific rows
    
    
    const channels = supabase.channel('custom-filter-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: '*', schema: 'public', table: 'solar_assessments', filter: 'some_column=eq.some_value' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()
Columns

| Name | Format | Type | Description | 
| ---- | ---- | ---- | ----  |
| id | 

uuid

 | string |  | 
| title | 

text

 | string |  | 
| address | 

text

 | string |  | 
| city | 

text

 | string |  | 
| state | 

text

 | string |  | 
| zipcode | 

text

 | string |  | 
| status | 

text

 | string |  | 
| solar_api_id | 

text

 | string |  | 
| client_name | 

text

 | string |  | 
| client_email | 

text

 | string |  | 
| client_phone | 

text

 | string |  | 
| created_at | 

timestamp with time zone

 | string |  | 
| updated_at | 

timestamp with time zone

 | string |  | 
| group_id | 

uuid

 | string |  | 
| lat | 

double precision

 | number |  | 
| lng | 

double precision

 | number |  | 
| project_stage_id | 

uuid

 | string |  | 
| workflow_template_id | 

uuid

 | string |  | 
| stage_updated_at | 

timestamp with time zone

 | string |  | 
| client_id | 

uuid

 | string |  | 
| place_id | 

text

 | string |  | 
| input_approx_utility_bill | 

numeric

 | number |  | 
| utility_rate_kwh | 

double precision

 | number |  | 

## Read rows

[Documentation](https://supabase.com/docs/reference/javascript/select)

To read rows in this table, use the `select` method.

Read all rows
    
    
    let { data: projects, error } = await supabase
    
      .from('projects')
    
      .select('*')

Read specific columns
    
    
    let { data: projects, error } = await supabase
    
      .from('projects')
    
      .select('some_column,other_column')

Read referenced tables
    
    
    let { data: projects, error } = await supabase
    
      .from('projects')
    
      .select(`
    
        some_column,
    
        other_table (
    
          foreign_key
    
        )
    
      `)

With pagination
    
    
    let { data: projects, error } = await supabase
    
      .from('projects')
    
      .select('*')
    
      .range(0, 9)

## Filtering

[Documentation](https://supabase.com/docs/reference/javascript/using-filters)

Supabase provides a wide range of filters

With filtering
    
    
    let { data: projects, error } = await supabase
    
      .from('projects')
    
      .select("*")
    
    
    
    
      // Filters
    
      .eq('column', 'Equal to')
    
      .gt('column', 'Greater than')
    
      .lt('column', 'Less than')
    
      .gte('column', 'Greater than or equal to')
    
      .lte('column', 'Less than or equal to')
    
      .like('column', '%CaseSensitive%')
    
      .ilike('column', '%CaseInsensitive%')
    
      .is('column', null)
    
      .in('column', ['Array', 'Values'])
    
      .neq('column', 'Not equal to')
    
    
    
    
      // Arrays
    
      .contains('array_column', ['array', 'contains'])
    
      .containedBy('array_column', ['contained', 'by'])
    
    
    
    
      // Logical operators
    
      .not('column', 'like', 'Negate filter')
    
      .or('some_column.eq.Some value, other_column.eq.Other value')

## Insert rows

[Documentation](https://supabase.com/docs/reference/javascript/insert)

`insert` lets you insert into your tables. You can also insert in bulk and do UPSERT.

`insert` will also return the replaced values for UPSERT.

Insert a row
    
    
    const { data, error } = await supabase
    
      .from('projects')
    
      .insert([
    
        { some_column: 'someValue', other_column: 'otherValue' },
    
      ])
    
      .select()

Insert many rows
    
    
    const { data, error } = await supabase
    
      .from('projects')
    
      .insert([
    
        { some_column: 'someValue' },
    
        { some_column: 'otherValue' },
    
      ])
    
      .select()

Upsert matching rows
    
    
    const { data, error } = await supabase
    
      .from('projects')
    
      .upsert({ some_column: 'someValue' })
    
      .select()

## Update rows

[Documentation](https://supabase.com/docs/reference/javascript/update)

`update` lets you update rows. `update` will match all rows by default. You can update specific rows using horizontal filters, e.g. `eq`, `lt`, and `is`.

`update` will also return the replaced values for UPDATE.

Update matching rows
    
    
    const { data, error } = await supabase
    
      .from('projects')
    
      .update({ other_column: 'otherValue' })
    
      .eq('some_column', 'someValue')
    
      .select()

## Delete rows

[Documentation](https://supabase.com/docs/reference/javascript/delete)

`delete` lets you delete rows. `delete` will match all rows by default, so remember to specify your filters!

Delete matching rows
    
    
    const { error } = await supabase
    
      .from('projects')
    
      .delete()
    
      .eq('some_column', 'someValue')

## Subscribe to changes

[Documentation](https://supabase.com/docs/reference/javascript/subscribe)

Supabase provides realtime functionality and broadcasts database changes to authorized users depending on Row Level Security (RLS) policies.

Subscribe to all events
    
    
    const channels = supabase.channel('custom-all-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: '*', schema: 'public', table: 'projects' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to inserts
    
    
    const channels = supabase.channel('custom-insert-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: 'INSERT', schema: 'public', table: 'projects' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to updates
    
    
    const channels = supabase.channel('custom-update-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: 'UPDATE', schema: 'public', table: 'projects' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to deletes
    
    
    const channels = supabase.channel('custom-delete-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: 'DELETE', schema: 'public', table: 'projects' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()

Subscribe to specific rows
    
    
    const channels = supabase.channel('custom-filter-channel')
    
      .on(
    
        'postgres_changes',
    
        { event: '*', schema: 'public', table: 'projects', filter: 'some_column=eq.some_value' },
    
        (payload) => {
    
          console.log('Change received!', payload)
    
        }
    
      )
    
      .subscribe()
