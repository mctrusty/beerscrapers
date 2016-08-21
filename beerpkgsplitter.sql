CREATE TYPE pkg_params AS (
	sz numeric(5,2),
	txt text,
	container text
);

CREATE OR REPLACE FUNCTION split_pkg_col(qtytxt text)
RETURNS pkg_params
AS $$
	import re
	match = re.search('(\d+(?:.\d+)?)(.*)', qtytxt)
	if match:
		sz = match.group(1)
		txt = match.group(2)
		return [sz, txt, '']
	return None
$$ LANGUAGE plpythonu;

CREATE OR REPLACE FUNCTION split_qty_col(sztxt text)
RETURNS pkg_params
AS $$
	import re
	match = re.search('(\d+(?:.\d+)?)(OZ|ML)?(.*)', sztxt)
	if match:
		sz = match.group(1)
		txt = match.group(2)
		container = match.group(3)
		return [sz, txt, container]
	return None
$$ LANGUAGE plpythonu;
