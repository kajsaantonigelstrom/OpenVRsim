//========= Copyright 2020, Anton. All rights reserved. ===========
using System;
using System.Runtime.InteropServices;

namespace AntonSound
{
	public static class AntonSound_API
	{
		/// <summary>
		/// Initiate the Asset.
		/// </summary>
		/// <returns>true : everything ok</returns>
		[DllImport("AntonSoundPlayer")]
		public static extern bool Initiate();

		/// <summary>
		/// Load a wav-file.
		/// </summary>
		/// <returns>true : everything ok</returns>
		[DllImport("AntonSoundPlayer")]
		public static extern bool LoadSound(String filename);

		
		/// <summary>
		/// Play the loaded sound.
		/// </summary>
		/// <returns>true : everything ok</returns>
		[DllImport("AntonSoundPlayer")]
		public static extern bool DoPlaySound(int delay_ms);

		/// <summary>
		/// Close the SoundPlayer
		/// </summary>
		/// <returns>true : everything ok</returns>
		[DllImport("AntonSoundPlayer")]
		public static extern bool Close();

		// Interface to sound process
		[DllImport("AntonSoundPlayer")]
		public static extern bool LoadSoundProcess(String filename);

		[DllImport("AntonSoundPlayer")]
		public static extern bool RunSoundProcess(int delay_ms);

	}
}


