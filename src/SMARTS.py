def create_run_smarts_input_file_dni(
        air_mass,
        water_vapor,
        l_o3,
        aod,       
        smarts_folder,
        smarts_file,
        filter_= 1,wvl_min=300, wvl_max=1100,step=0.5,fwhm=7, 
        epsilon=1,
        pressure=1013.25,
        aerosol_type="'S&F_RURAL'",
        aod_variable=0,
        G_sc=1366.1,
        no_of_variables=1,
        actual_variable=2,
):
    
    """
    Creates and runs a SMARTS input file for simulation or calculation related to atmospheric parameters and solar irradiance.

    Parameters:
    -----------
    air_mass : float
        Atmospheric air mass representing the path length of sunlight through the atmosphere.
    water_vapor : float
        Amount of water vapor content in the atmosphere, measured in g/cm^2.
    l_o3 : float
        Ozone layer thickness in cm.
    aod : float
        Aerosol optical depth.
    smarts_folder : str
        Directory path where the SMARTS software files are located.
    smarts_file : str
        Path to the specific SMARTS input file to be modified and run.
    filter_ : int, optional
        Filtering parameter (default is 1), depending on the instrument: 1 for gaussian spectroradiometer filtering, 0 for triangular filtering.
    wvl_min : int, optional
        Minimum wavelength of the spectroradiometer (default is 300 nm).
    wvl_max : int, optional
        Maximum wavelength of the spectroradiometer (default is 1100 nm).
    step : float, optional
        Step size for the smoothed spectral irradiance, that simulates the spectroradiometer (default is 0.5 nm).
    fwhm : int, optional
        Full width at half maximum for spectral resolution of the spectroradiometer (default is 7 nm).
    epsilon : int, optional
        Earth-Sun distance correction (defaulted to 1).
    pressure : float, optional
        Atmospheric pressure in hPa (defaulted to 1013.25 hPa/mbar).
    aerosol_type : str, optional
        Type of aerosol model (default is 'S&F_RURAL', options are provided in SMARTS2 documentation).
    aod_variable : int, optional
        Aerosol optical depth variable type (default is 0 for AOD at 500 nm, 1 for Angstrom turbidity, 5 for AOD at 550 nm, other options are provided in SMARTS2 documentation).
    G_sc : float, optional
        Solar constant in W/m² (default is 1366.1 W/m²).
    no_of_variables : int, optional
        Number of variables considered in calculation (defaulted to 1).
    actual_variable : int, optional
        Specific variable to be used in calculation (default is 2, corresponding to DNI, other options are provided in SMARTS2 documentation).

    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the following columns from the processed SMARTS output file:

        - WVLGTH: Wavelength in nanometers (nm).
        - ET_SPCTRUM: Extraterrestrial spectrum.
        - BEAM_NORMAL: Direct normal irradiance.
        - BEAM_NORM+: Circumsolar irradiance, if geometric correction is necessary.
        - GLOB_HORIZ: Global horizontal irradiance.
        - GLOBL_TILT: Global tilted irradiance.

    Notes:
    ------
    The function modifies a SMARTS input file according to the given parameters, runs the
    SMARTS executable, processes the resulting data, and cleans up temporary output files.

    Example:
    --------
    >>> data = create_run_smarts_input_file_dni(
    ...     air_mass=1.5,
    ...     water_vapor=2.0,
    ...     l_o3=0.3,
    ...     aod=0.1,
    ...     smarts_folder='./smarts/',
    ...     smarts_file='./smarts/input.txt'
    ... )
    """
    
    new_lines = []  # To store modified lines
    with open(smarts_file, 'r') as txt:
        text = txt.readlines()
        for index, line in enumerate(text):
            if index == 2:
                new_lines.append(str(pressure) + '\n')
            elif index == 6:
                new_lines.append(str(water_vapor) + '\n')
            elif index == 8:
                new_lines.append('0 '+str(l_o3) + '\n')
            elif index == 12:
                new_lines.append(str(aerosol_type) + '\n')
            elif index == 13:
                new_lines.append(str(aod_variable) + '\n')
            elif index == 14:
                new_lines.append(str(aod) + '\n')
            elif index == 17:
                new_lines.append('280 4000 ' + str(epsilon) + ' ' + str(G_sc) + '\n')
            elif index == 20:
                new_lines.append(str(no_of_variables) + '\n')
            elif index == 21:
                new_lines.append(str(actual_variable) +'\n')
            elif index == 24:
                new_lines.append(str(filter_)+' '+str(wvl_min)+' '+str(wvl_max)+' '+str(step)+' '+str(fwhm)+' !Card 14a \n')
            elif index == 28:
                new_lines.append(str(air_mass) +'\n')
            else:
                new_lines.append(line)  # Keep the original line

    with open(smarts_file, 'w') as txt:
        txt.writelines(new_lines)
    command = 'smarts295bat.exe'
    os.chdir(smarts_folder)
    process = subprocess.call(command)

    data = pd.read_fwf('smarts295.scn.txt',skiprows=2)
    #Output files must be renamed or removed to run SMARTS2 again
    try:
        os.remove('smarts295.out.txt')
    except:
        pass
    try: 
        os.remove('smarts295.ext.txt')
    except:
        pass
    try:
        os.remove('smarts295.scn.txt')
    except:
        pass
    return(data)