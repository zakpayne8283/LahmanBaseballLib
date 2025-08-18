# Database Wrappers
To use the database wrappers, simply import which table you want to use:
<pre>from db.models.People import People</pre>
Then you can run queries against the class using methods, similar to the SQL syntax:
<pre>People.select().where(nameFirst="Hank", nameLast="Aaron").execute()</pre>
Which will return a `List<People>` object corresponding to each found object, which can then be used an object:
<pre>
# Query
results = People.select().where(nameLast="Judge").execute()

# Print Results
for player in results:
    print(f"{player.nameFirst} {player.nameLast}")

=== OUTPUTS ===
Aaron Judge
Joe Judge
</pre>

## Available Methods

`TableBase.select(*columns)`

**Returns**: `Query()`
**Description**: Initialize a new `Query` for the class, optionally specifying the columns. **Required to run a query.**
**Parameters**:
- `*columns`: Optional columns passed as `strings`.

**Example**:
<pre>
People.select("nameFirst", "nameLast", "playerID").execute()

=== OUTPUT ===
David	Aardsma	aardsda01
Hank	Aaron	aaronha01
Tommie	Aaron	aaronto01
[...]
</pre>