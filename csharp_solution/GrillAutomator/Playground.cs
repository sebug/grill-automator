using System;
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

        public void Detect()
        {

        }
    }
}
