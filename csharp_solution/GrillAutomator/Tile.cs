using System;
namespace GrillAutomator
{
    public class Tile
    {
        public string TilePath { get; }
        public Tile(string tilePath)
        {
            this.TilePath = tilePath ?? throw new ArgumentNullException(nameof(tilePath));
        }
    }
}
