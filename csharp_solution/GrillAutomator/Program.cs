using System;

namespace GrillAutomator
{
    class MainClass
    {
        public static int Main(string[] args)
        {
            if (args.Length <= 1)
            {
                Console.Error.WriteLine("Usage: GrillAutomator image.png tiles_directory");
                return 1;
            }
            return 0;
        }
    }
}
