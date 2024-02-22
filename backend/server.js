const neo4j = require('neo4j-driver');

const uri = 'neo4j://<host>:<port>';
const user = '<username>';
const password = '<password>';

const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));

async function findClosestBikeParks(lat, lon) {
    const session = driver.session();
    try {
      const result = await session.run(
        'MATCH (p:BikePark) \
         RETURN p, distance(point({latitude: $lat, longitude: $lon}), p.location) AS dist \
         ORDER BY dist ASC \
         LIMIT 5',
        { lat, lon }
      );
  
      return result.records.map(record => ({
        id: record.get('p').identity.low,
        name: record.get('p').properties.name,
        distance: record.get('dist')
      }));
    } finally {
      await session.close();
    }
  }
  