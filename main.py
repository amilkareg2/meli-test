import functions_framework
from collections import defaultdict
from flask import jsonify
from google.cloud import bigquery

MIN_REPEATED = 4
query = """
SELECT
  COUNTIF(is_mutant = TRUE) AS count_mutant_dna,
  COUNTIF(is_mutant = FALSE) AS count_human_dna,
  SAFE_DIVIDE(COUNTIF(is_mutant = TRUE), COUNT(*)) AS ratio
FROM
  `colvending.meli.stats`

    """
client = bigquery.Client()
dataset_id = 'meli' 
table_id = 'stats'

def parse_dna(matrix):
  rows = defaultdict(list)
  cols = defaultdict(list)
  diags = defaultdict(list)
  inv_diags = defaultdict(list)

  for i, row in enumerate(matrix):
    for j, val in enumerate(row):
        rows[i].append(val)
        cols[j].append(val)
        diags[i-j].append(val)
        inv_diags[i+j-(len(matrix)-1)].append(val)
  
  return rows, cols, diags, inv_diags

def get_count(seqs):
    seq_count = 0
    for s in seqs:
        if len(s) >= MIN_REPEATED:
            let_count = 1
            for i in range(1, len(s)):
                if s[i] == s[i-1]:
                    let_count += 1
                    if let_count >= MIN_REPEATED:
                        seq_count += 1
                        break
                else:
                    let_count = 1
        if seq_count >= 2:
          return True
    return False 


@functions_framework.http
def main(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    if request.path == '/mutant' and 'dna' in request_json:
        dna = request_json['dna']
        total = [v for seq in parse_dna(dna) for v in seq.values()]
        rsp = get_count(total)
        rows_to_insert = [{"record": dna, "is_mutant": rsp}]
        table_ref = client.dataset(dataset_id).table(table_id)
        client.insert_rows_json(table_ref, rows_to_insert)
        if rsp:
            return jsonify({"message": "Request processed successfully!"}), 200
        else:
            return jsonify({"error": "Forbidden", "message": "You are not authorized."}), 403
    if request.path == '/stats':
        try:
            job_config = bigquery.QueryJobConfig()
            query_job = client.query(query, job_config=job_config)

            # Wait for the query to finish and fetch the result
            results = query_job.result()  # Wait for job to complete

            # Extract the counts and ratio from the results
            for row in results:
                mutant_count = row["count_mutant_dna"]
                non_mutant_count = row["count_human_dna"]
                mutant_ratio = row["ratio"]

            # Return the counts and ratio as JSON
            return jsonify({
                "count_mutant_dna": mutant_count,
                "count_human_dna": non_mutant_count,
                "ratio": mutant_ratio
            }), 200
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500
        

    return jsonify({"error": "Bad Request", "message": "Invalid data or endpoint."}), 400
