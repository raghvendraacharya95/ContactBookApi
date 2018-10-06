ADD_NEW_CONTACT = """
INSERT INTO contact_detail_master(first_name,last_name,phone_number,email_id)
VALUES(%s,%s,%s,%s);
"""

CHECK_PHONE_NUMBER_EXISTS = """
SELECT * FROM contact_detail_master WHERE phone_number = %s
"""

CHECK_EMAIL_EXISTS = """
SELECT * FROM contact_detail_master WHERE email_id = %s
"""

CHECK_CONTACT_ID_EXISTS = """
SELECT phone_number FROM contact_detail_master WHERE id = %s
"""

GET_CONTACT_DETAILS = """
SELECT * FROM contact_detail_master WHERE id = %s
"""

UPDATE_CONTACT_DETAILS = """
UPDATE contact_detail_master SET first_name = %s,last_name = %s,phone_number = %s,email_id = %s WHERE id = %s
"""

REMOVE_CONTACT = """
DELETE FROM contact_detail_master WHERE id = %s
"""

GET_CONTACT_DETAILS_BY_FIRST_NAME = """
SELECT * FROM contact_detail_master WHERE first_name = %s
"""

GET_CONTACT_DETAILS_BY_LAST_NAME = """
SELECT * FROM contact_detail_master WHERE last_name = %s
"""

GET_CONTACT_DETAILS = """
SELECT * FROM contact_detail_master LIMIT %s
"""