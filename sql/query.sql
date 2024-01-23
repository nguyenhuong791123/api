SELECT p.page_id,
p.page_key,
p.page_auth::jsonb,
l.object_label::jsonb->>'ja' AS page_name
,json_agg(f.fields) FROM(
SELECT
f.page_id
,json_build_object(
'field', p.properties_name
,'view', p.value::jsonb->'auth'->'view'
,'label', pl.object_label::jsonb->>'ja'
,'type', substring(p.properties_name, 0, position('_' IN p.properties_name))
) AS fields
FROM mente.form_info f
LEFT JOIN mente.schema_info s ON f.form_id=s.form_id
LEFT JOIN mente.properties_info p ON p.schema_id=s.schema_id
INNER JOIN mente.label_info pl ON pl.properties_name=p.properties_name
) AS f
INNER JOIN mente.page_info p ON p.page_id=f.page_id
LEFT JOIN mente.label_info l ON l.properties_name=p.page_id::varchar
WHERE p.company_id=1 AND p.page_deleted=0 AND p.page_id=1054
GROUP BY p.page_id, l.object_label