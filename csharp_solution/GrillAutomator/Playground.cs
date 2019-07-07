using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace GrillAutomator
{
    public class Playground
    {
        public string ImagePath { get; }
        public string TilesPath { get; }
        public Playground(string imagePath,
            string tilesPath)
        {
            this.ImagePath = imagePath ?? throw new ArgumentNullException(nameof(imagePath));
            this.TilesPath = tilesPath ?? throw new ArgumentNullException(nameof(tilesPath));
        }

        private IEnumerable<Tile> GetTiles()
        {
            var files = Directory.EnumerateFiles(this.TilesPath, "*.png");
            return files.Select(p => new Tile(p));
        }

        public void Detect()
        {
            var tiles = this.GetTiles().ToList();
        }
    }
}
