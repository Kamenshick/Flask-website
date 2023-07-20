 let map;

  main();
  async function main() {
      await ymaps3.ready;

      map = new ymaps3.YMap(document.getElementById('map'), {
          location: {
              // Координаты центра карты
              // Порядок по умолчанию: «долгота, широта»
              center: [132.924746,48.789920],
              zoom: 10
          }
      });

      map.addChild(new ymaps3.YMapDefaultSchemeLayer());
  }