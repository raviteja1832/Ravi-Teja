import sys
choice = int(input("Enter the Choice, Enter 1 to Run Indian Standard (IS )CODE or   Enter 2 to Run American Concrete Institute(ACI) CODE :"))
if choice==1:
    # IS 456:2000 Table 5 | "Exposure condition": [Minimum cement content in kg/m^3, Maximum water to cement ratio] 
    IS456_t5 = { "Mild": [300, 0.55], "Moderate": [300, 0.50], "Severe": [320, 0.45], "Very severe": [340, 0.45], "Extreme": [360, 0.40] }

    # IS 10262:2009 Table 1 | "Grade": Assumed Standard Deviation
    IS10262_t1 = { "M1": 3.5, "M2": 4.0, "M3": 5.0, "M4": 6.0 }
    IS10262_t11 = { "M1": 5.0, "M2": 5.5, "M3": 6.5, "M4": 8.0 }

    # IS 10262:2009 Table 2 | "Nominal Maximum Size of Aggregate in mm": Maximum Water content in kg
    IS10262_t2 = { "10": 208, "20": 186, "40": 165 }

    # IS 10262:2009 Table 3 | "Nominal Maximum Size of Aggregate in mm": (vol of coarse aggregates)[Zone 4, Zone 3, Zone 2, Zone 1]
    IS10262_t3 = { "10": [0.54, 0.52, 0.50, 0.48], "20": [0.66, 0.64, 0.62, 0.60], "40": [0.73, 0.72, 0.71, 0.69] }

    air_content = {'10': 1.5, '20': 1.0, '40': 0.8}

    def target_strength_calculation(grade):
        """Target Strength for Mix Proportioning"""
        if grade == "M 10" or grade == "M 15":
            g = "M1"
        elif grade == "M 20" or grade == "M 25":
            g = "M2"
        elif int(grade[1:])>=30 and int(grade[1:])<=60:
            g = "M3"
        else:
            g = "M4"
        
        sd = IS10262_t1[g]
        X = IS10262_t11[g]
        
        return max((int(grade[1:])+(1.65*sd)), (int(grade[1:])+X))

    def water_cement_ratio_calculation(exposure):
        """Selection of Water Cement Ratio"""
        exp = exposure.capitalize()
        for x, v in IS456_t5.items():
            if x == exp:
                wcr = v[1]
        return wcr

    def water_content_calculation(slump, soa, toa, chem_ad):
        """Selection of Water Content"""
        # Factor for convertion of water content of 50 mm slump to required slump
        n = (int(slump) - 50) / 25
        for x, v in IS10262_t2.items():
            if x == soa:
                water_content = v
        if toa == "Sub-Angular":
            water_content -= 10
        elif toa == "Gravel":
            water_content -= 15
        elif toa == "Rounded Gravel":
            water_content -= 20
        
        if int(slump) > 50:
            water_content += (0.03 * n * water_content)

        if chem_ad == "Super Plasticizer":
            water_content -= water_content * 0.23
        elif chem_ad == "Plasticizer":
            water_content -= water_content * 0.1
        return water_content

    def cement_content_calculation(exposure, wcr, wc):
        """Calculation of Cement Content"""
        exp = exposure.capitalize()
        for x, v in IS456_t5.items():
            if x == exp:
                min_cc = v[0]
        
        cement_content = wc/wcr

        if cement_content < min_cc:
            cement_content = min_cc
        
        return cement_content

    def fly_cement_content_calculation(exposure, wcr, wc):
        """Calculation of Cement and Fly Ash Content"""
        exp = exposure.capitalize()
        for x, v in IS456_t5.items():
            if x == exp:
                min_cc = v[0]
        
        cement_content = wc/wcr
        temp1 = cement_content

        if cement_content < min_cc:
            cement_content = min_cc
            temp1 = cement_content
        cement_content *= 1.10
        new_water_cement_ratio = wc/cement_content
        flyash_content = cement_content * 0.3
        temp2 = cement_content
        temp2 -= flyash_content

        if temp2 < 270:
            i = 0.25
            while True and i > 0:
                temp2 = cement_content
                flyash_content = temp2 * i
                temp2 -= flyash_content
                i -= 0.05
                if temp2 >= 270:
                    print("\nPercentage of Fly Ash is {}%\n".format(int((i+0.05)*100)))
                    break
                elif i < 0:
                    sys.exit("Mix is not possible!!(Cement < 270)")
        cement_content = temp2
        cement_saved = temp1 - cement_content
        return cement_content, flyash_content, cement_saved, new_water_cement_ratio

    def vol_of_CAnFA_calculation(zone, soa, wcr, pumping):
        """Proportion of Volume of Coarse Aggregate And Fine Aggregate Content"""
        if zone == "Zone 4":
            i = 0
        elif zone == "Zone 3":
            i = 1
        elif zone == "Zone 2":
            i = 2
        elif zone == "Zone 1":
            i = 3
        
        for x, v in IS10262_t3.items():
            if x == soa:
                vol_CA = v[i]
        
        if wcr > 0.5:
            vol_CA -= 0.01*((wcr - 0.5)/0.05)
        else:
            vol_CA += 0.01*((0.5 - wcr)/0.05)

        if pumping == True:
            vol_CA *= 0.9
        
        vol_FA = 1 - vol_CA
        
        return vol_CA, vol_FA

    def mix_calculation(cc, sp_c, wc, v_ca, v_fa, sp_ca, sp_fa, sp_chemad):
        """Mix Calculations per unit volume of concrete"""
        # Volume of cement
        vol_cement = (cc/sp_c) * 0.001
        print("\nVolume of cement = {:.4f} m^3".format(vol_cement))

        # Volume of water
        vol_water = wc * 0.001
        print("\nVolume of water = {:.4f} m^3".format(vol_water))

        # Volume of Chemical Admixture @ 1% by cementitious material
        mass_of_chemAd = cc * 0.01
        vol_chemAd = (mass_of_chemAd / sp_chemad) * 0.001
        print("\nVolume of Chemical Admixture = {:.4f} m^3".format(vol_chemAd))

        # Volume of all in aggregate
        vol_all_aggr = ((1-(air_content[SIZE_OF_AGGREGATE]/100)) - (vol_cement + vol_water + vol_chemAd))
        print("\nVolume of all in aggregate = {:.4f} m^3".format(vol_all_aggr))

        # Mass of Coarse aggregate
        mass_CA = vol_all_aggr * v_ca * sp_ca * 1000

        # Mass of Fine aggregate
        mass_FA = vol_all_aggr * v_fa * sp_fa * 1000

        return mass_of_chemAd, mass_CA, mass_FA

    def fly_mix_calculation(cc, sp_c, wc, v_ca, v_fa, sp_ca, sp_fa, sp_fly, sp_chemad, fc):
        """Mix Calculations per unit volume of concrete"""
        # Volume of cement
        vol_cement = (cc/sp_c) * 0.001
        print("\nVolume of cement = {:.4f} m^3".format(vol_cement))

        # Volume of fly ash
        vol_flyash = (fc/sp_fly) * 0.001
        print("\nVolume of fly ash = {:.4f} m^3".format(vol_flyash))

        # Volume of water
        vol_water = wc * 0.001
        print("\nVolume of water = {:.4f} m^3".format(vol_water))

        # Volume of Chemical Admixture @ 2% by cementitious material
        mass_of_chemAd = cc * 0.02
        vol_chemAd = (mass_of_chemAd / sp_chemad) * 0.001
        print("\nVolume of Chemical Admixture = {:.4f} m^3".format(vol_chemAd))

        # Volume of all in aggregate
        vol_all_aggr = ((1-(air_content[SIZE_OF_AGGREGATE]/100)) - (vol_cement + vol_flyash + vol_water + vol_chemAd))
        print("\nVolume of all in aggregate = {:.4f} m^3".format(vol_all_aggr))

        # Mass of Coarse aggregate
        mass_CA = vol_all_aggr * v_ca * sp_ca * 1000

        # Mass of Fine aggregate
        mass_FA = vol_all_aggr * v_fa * sp_fa * 1000

        return mass_of_chemAd, mass_CA, mass_FA

    # Input from user and calling the fuction

    GRADE = input("\nEnter the Grade Designition (eg: M 40): ")
    GRADE = GRADE.upper()
    if len(GRADE) == 3:
        GRADE = GRADE.replace('M', 'M ',)

    print("\nWhich mineral admixture are you using?")
    print("""[1] None  [2] Fly ash""")
    min_ad = input("Choise (eg: 2): ")
    if min_ad == '1':
        TYPE_OF_MINERAL_ADMIXTURE = ''
    elif min_ad == '2':
        TYPE_OF_MINERAL_ADMIXTURE = "Fly ash"

    SIZE_OF_AGGREGATE = input("\nEnter the maximum nominal size of aggregate in mm [10,20,40]: ")

    WORKABILITY = input("Enter the workability(slump) of cement in mm [Eg: 100]: ")

    EXPOSURE_CONDITION = input("Enter the Exposure Condition (Eg: Moderate): ")

    METHOD_OF_PLACING = input("Will you Pump the Concrete? (Yes or No): ")
    while True:
        if METHOD_OF_PLACING.lower() == 'yes':
            pumping = True
            break
        elif METHOD_OF_PLACING.lower() == 'no':
            pumping = False
            break
        else:
            print("Invalid Input!!")
        METHOD_OF_PLACING = input("Will you pump the concrete? (Yes or No): ")

    print("\nSelect the type of aggregate:")
    print("""[1] Sub-Angular, [2] Gravel, [3] Rounded gravel, [4] Crushed Angular""")
    TYPE_OF_AGGREGATE = input("Choice (Eg: 4): ")
    if TYPE_OF_AGGREGATE == "1":
        toa = "Sub-Angular"
    elif TYPE_OF_AGGREGATE == "2":
        toa = "Gravel"
    elif TYPE_OF_AGGREGATE == "3":
        toa = "Rounded gravel"
    else:
        toa = ''

    print("\nSelect the type of Admixture:")
    print(""" [1] Super Plasticizer, [2] Plasticizer """)
    CHEMICAL_ADMIXTURE = input("Choice (eg: 1): ")
    if CHEMICAL_ADMIXTURE == "1":
        chem_ad = "Super Plasticizer"
    elif CHEMICAL_ADMIXTURE == "2":
        chem_ad = "Plasticizer"

    SP_CEMENT = float(input("\nEnter specific gravity of Cement: "))

    if TYPE_OF_MINERAL_ADMIXTURE == "Fly ash":
        SP_ADMIX = float(input("Enter specific gravity of Fly-Ash: "))
    SP_CA = float(input("Enter specific gravity of Coarse Aggregate: "))
    SP_FA = float(input("Enter specific gravity of Fine Aggregate: "))
    SP_CHEMAD = float(input("Enter Specific Gravity of Admixture: "))
    WATER_ABSORPTION_CA = float(input("Enter the Water Absorption of Coarse aggregates: "))
    WATER_ABSORPTION_FA = float(input("Enter the Water Absorption of FINE aggregates: "))
    print("\nSelect the Zone of Fine Aggregates: ")
    print("""  [1] Zone 1, {2] Zone 2, [3] Zone 3,[4] Zone 4  """)
    ZONE_OF_FA = input("Choice: ")
    if ZONE_OF_FA == '1':
        zone = "Zone 1"
    elif ZONE_OF_FA == '2':
        zone = "Zone 2"
    elif ZONE_OF_FA == '3':
        zone = "Zone 3"
    elif ZONE_OF_FA == '4':
        zone = "Zone 4"
    # Checking whether to Surface moisturein aggregates is present or not
    CA_SURFACE_MOISTURE = input("\nIs surface moisture present in the Coarse Aggregates? (Yes or No): ")
    CA_SURF_MOISTURE = 0.0
    while True:
        if CA_SURFACE_MOISTURE.lower() == 'yes':
            CA_SURF_MOISTURE = float(input("Enter the surface moisture of Coarse aAgregates: "))
            break
        elif CA_SURFACE_MOISTURE.lower() == 'no':
            break
        else:
            print("Invalid Input!!")
        CA_SURFACE_MOISTURE = input("Is surface moisture present in the Coarse aAgregates? (yes or no): ")

    FA_SURFACE_MOISTURE = input("\nIs surface moisture present in the Fine Aggregate ? (yes or no): ")
    FA_SURF_MOISTURE = 0.0
    while True:
        if FA_SURFACE_MOISTURE.lower() == 'yes':
            FA_SURF_MOISTURE = float(input("Enter the surface moisture of Fine Aggregate : "))
            break
        elif FA_SURFACE_MOISTURE.lower() == 'no':
            break
        else:
            print("Invalid Input!!")
        FA_SURFACE_MOISTURE = input("Is surface moisture present in the Fine Aggregate ? (yes or no): ")
    # Printing the results
    print("\n################################################################################")
    TARGET_STRENGTH = target_strength_calculation(GRADE)
    print("\nTarget strength = {} N/mm^2".format(TARGET_STRENGTH))
    WATER_CEMENT_RATIO = water_cement_ratio_calculation(EXPOSURE_CONDITION)
    WATER_CONTENT = water_content_calculation(WORKABILITY, SIZE_OF_AGGREGATE, toa, chem_ad)
    if TYPE_OF_MINERAL_ADMIXTURE == '':
        CEMENT_CONTENT = cement_content_calculation(EXPOSURE_CONDITION, WATER_CEMENT_RATIO, WATER_CONTENT)

        VOL_CA, VOL_FA = vol_of_CAnFA_calculation(zone, SIZE_OF_AGGREGATE, WATER_CEMENT_RATIO, pumping)
        print("\nProportion of Volume of Coarse Aggregate  is {:.2f} and of Fine Aggregate  is {:.2f}".format(VOL_CA, VOL_FA))

        MASS_CHEM_AD, MASS_CA, MASS_FA = mix_calculation(CEMENT_CONTENT, SP_CEMENT, WATER_CONTENT, VOL_CA, VOL_FA, SP_CA, SP_FA, SP_CHEMAD)

        print("\nMix Proportions for this Trial:")
        print("""
                1. Cement               =   {:.2f} kg/m^3
                2. Water                =   {:.2f} lit
                3. Fine Aggregate       =   {:.2f} kg
                4. Coarse Aggregate     =   {:.2f} kg
                5. Chemical admixture   =   {:.2f} kg/m^3
                6. Water-cement ratio   =   {}
        """.format(CEMENT_CONTENT, WATER_CONTENT, MASS_FA, MASS_CA, MASS_CHEM_AD, WATER_CEMENT_RATIO))
        
    else:
        CEMENT_CONTENT, FLYASH_CONTENT, CEMENT_SAVED, NEW_WATER_CEMENT_RATIO = fly_cement_content_calculation(EXPOSURE_CONDITION, WATER_CEMENT_RATIO, WATER_CONTENT)
        print("Cement saved while using flyash is {:.2f} kg/m^3".format(CEMENT_SAVED))

        VOL_CA, VOL_FA = vol_of_CAnFA_calculation(zone, SIZE_OF_AGGREGATE, WATER_CEMENT_RATIO, pumping)
        print("\nProportion of Volume of Coarse AGGREGATE is {:.2f} and of FINE AGGREGATE is {:.2f}".format(VOL_CA, VOL_FA))

        MASS_CHEM_AD, MASS_CA, MASS_FA = fly_mix_calculation(CEMENT_CONTENT, SP_CEMENT, WATER_CONTENT, VOL_CA, VOL_FA, SP_CA, SP_FA, SP_ADMIX, SP_CHEMAD, FLYASH_CONTENT)

        print("\nMix Proportions for this trial:")
        print("""
                1. Cement               =   {:.2f} kg/m^3
                2. Flyash               =   {:.2f} kg/m^3
                3. Water                =   {:.2f} lit
                4. Fine aggregate       =   {:.2f} kg
                5. Coarse aggregate     =   {:.2f} kg
                6. Chemical admixture   =   {:.2f} kg/m^3
                7. Water-cement ratio   =   {:.3f}
        """.format(CEMENT_CONTENT, FLYASH_CONTENT, WATER_CONTENT, MASS_FA, MASS_CA, MASS_CHEM_AD, NEW_WATER_CEMENT_RATIO))
    print("\nCorrection for Water absorption of aggregate:")
    CA_WA = MASS_CA * WATER_ABSORPTION_CA * 0.01
    FA_WA = MASS_FA * WATER_ABSORPTION_FA * 0.01
    print("""
                1. Coarse aggregate = {:.2f} lit
                2. Fine aggregate   = {:.2f} lit
    """.format(CA_WA, FA_WA))

    CA_SM = MASS_CA * CA_SURF_MOISTURE * 0.01
    FA_SM = MASS_FA * FA_SURF_MOISTURE * 0.01
    if CA_SURF_MOISTURE != 0.0 or FA_SURF_MOISTURE != 0.0:
        print("\nCorrection for Surface Moisture of aggregate:")
        print("""
                1. Coarse aggregate = {:.2f} lit
                2. Fine aggregate   = {:.2f} lit
        """.format(CA_SM, FA_SM))
    print("FREE WATER after final correction is {:.2f} lit\n".format((WATER_CONTENT + CA_WA + FA_WA - CA_SM - FA_SM)))
    print("Ratio = ",1," : ", (FLYASH_CONTENT)/(CEMENT_CONTENT), " : ", (MASS_FA)/(CEMENT_CONTENT), " : ", (MASS_CA)/(CEMENT_CONTENT), " : ", (WATER_CONTENT)/(CEMENT_CONTENT))
    print(" ~~~~~~~~~  Code Executed Successfully (Design By Rupesh Sir) ~~~~~~~~~")
elif choice==2:
    def water_content_calculation(h,i,j):
        table1_1 = {9.5: 207,12.5: 199,19.0: 190,25.0: 179,37.5: 166,50: 154,75.0: 130,150.0: 130}
        table1_2 = {9.5: 228,12.5: 216,19.0: 205,25.0: 193,37.5: 181,50: 169,75.0: 145,150.0: 125}
        table1_3 = {9.5: 243,12.5: 228,19.0: 216,25.0: 202,37.5: 190,50: 178,75.0: 160}
        table1_4 = {9.5: 181,12.5: 175,19.0: 168,25.0: 160,37.5: 150,50: 142,75.0: 122,150.0: 107}
        table1_5 = {9.5: 202,12.5: 193,19.0: 184,25.0: 175,37.5: 165,50: 157,75.0: 133,150.0: 119}
        table1_6 = {9.5: 216,12.5: 205,19.0: 197,25.0: 184,37.5: 174,50: 166,75.0: 154}
        if j=="non air entrained":
            if h >= 25.0 and h<=50.0:
                return table1_1[i]
            elif h>=75.0 and h<=100.0:
                return table1_2[i]
            else:
                return table1_3[i]
        else:
            if h >= 25.0 and h<=50.0:
                return table1_4[i]
            elif h>=75.0 and h<=100.0:
                return table1_5[i]
            else:
                return table1_6[i]
    def water_cement_ratio(k,j):
        table2_1 = {40.0: 0.42, 35.0: 0.47, 30.0: 0.54, 25.0: 0.61, 20.0: 0.69, 15.0: 0.79}
        table2_2 = {40.0: 0.36, 35.0: 0.39, 30.0: 0.45, 25.0: 0.52, 20.0: 0.6, 15.0: 0.7}
        if j=="non air entrained":
            if k in list(table2_1.keys()):
                return table2_1[k]
            else:
                l=k-(k%5.0)
                return ((table2_1[l+5]-table2_1[l])*((k-l)/(5.0)))+table2_1[l]
        else:
            if k in list(table2_1.keys()):
                return table2_2[k]
            else:
                l=k-(k%5.0)
                return ((table2_2[l+5]-table2_2[l])*((k-l)/(5.0)))+table2_2[l]
    def cement_content():
        return water_content_calculation(h,i,j)/water_cement_ratio(k,j)
    def volume_coarse_aggregate(i,f):
        table3_1 = {2.4: 0.5, 2.6: 0.48, 2.8: 0.46, 3.0:0.44}
        table3_2 = {2.4: 0.59, 2.6: 0.57, 2.8: 0.55, 3.0:0.53}
        table3_3 = {2.4: 0.66, 2.6: 0.64, 2.8: 0.62, 3.0:0.6}
        table3_4 = {2.4: 0.71, 2.6: 0.69, 2.8: 0.67, 3.0:0.65}
        table3_5 = {2.4: 0.75, 2.6: 0.73, 2.8: 0.71, 3.0:0.69}
        table3_6 = {2.4: 0.78, 2.6: 0.76, 2.8: 0.74, 3.0:0.72}
        table3_7 = {2.4: 0.82, 2.6: 0.8, 2.8: 0.78, 3.0:0.76}
        table3_8 = {2.4: 0.87, 2.6: 0.88, 2.8: 0.83, 3.0:0.81}
        if i == 9.5:
            return table3_1[f]*g
        elif i == 12.5:
            return table3_2[f]*g
        elif i == 19.0:
            return table3_3[f]*g
        elif i==25.0:
            return table3_4[f]*g
        elif i==37.5:
            #print(table3_5[f]*g)
            return table3_5[f]*g
        elif i == 50.0:
            return table3_6[f]*g
        elif i==75.0:
            return table3_7[f]*g
        elif i==150.0:
            return table3_8[f]*g
    def mass_basis(i,j):
        table4_1 = {9.5: 2280,12.5: 2310,19.0: 2345,25: 2380,37.5: 2410,50.0: 2445,75.0: 2490,150.0: 2530}
        table4_2 = {9.5: 2200,12.5: 2236,19.0: 2275,25: 2290,37.5: 2350,50.0: 2345,75.0: 2405,150.0: 2435}
        if j == "non air entrained":
            return (table4_1[i]-(cement_content()+water_content_calculation(h,i,j)+volume_coarse_aggregate(i,f)))
        else:
            return (table4_2[i]-(cement_content()+water_content_calculation(h,i,j)+volume_coarse_aggregate(i,f)))
    def volume_basis(i,j,m):
        table5_1 = {9.5: 3,12.5: 2.5,19.0: 2,25.0: 1.5,37.5: 1,50.0: 0.5,75.0: 0.3,150.0: 0.2}
        mild = {9.5: 4.5,12.5: 4,19.0: 3.5,25.0: 3,37.5: 2.5,50.0: 2,75.0: 1.5,150.0: 1}
        mode = {9.5: 6,12.5: 5.5,19.0: 5,25.0: 4.5,37.5: 4.5,50.0: 4,75.0: 3.5,150.0: 3}
        ext = {9.5: 7.5,12.5: 7,19.0: 6,25.0: 6,37.5: 5.5,50.0: 5,75.0: 4.5,150.0: 4}

        if j == "non air entrained":
            return (1-(water_content_calculation(h,i,j)/1000)+(cement_content()/(a*1000))+(volume_coarse_aggregate(i,f)/(b*1000))+(table5_1[i]*1000))*1000*d
        elif m == "mild":
            return (1-(water_content_calculation(h,i,j)/1000)+(cement_content()/(a*1000))+(volume_coarse_aggregate(i,f)/(b*1000))+(mild[i]*1000))*1000*d
        elif m == "moderate":
            return (1-(water_content_calculation(h,i,j)/1000)+(cement_content()/(a*1000))+(volume_coarse_aggregate(i,f)/(b*1000))+(mode[i]*1000))*1000*d
        elif m == "extreme":
            return (1-(water_content_calculation(h,i,j)/1000)+(cement_content()/(a*1000))+(volume_coarse_aggregate(i,f)/(b*1000))+(ext[i]*1000))*1000*d
    def step_8(i,j):
        table4_1 = {9.5: 2280,12.5: 2310,19.0: 2345,25.0: 2380,37.5: 2410,50.0: 2445,75.0: 2490,150.0: 2530}
        table4_2 = {9.5: 2200,12.5: 2236,19.0: 2275,25.0: 2290,37.5: 2350,50.0: 2345,75.0: 2405,150.0: 2435}
        print("----------------------------------------------------------------------------------------------------")
        print("Coarse Aggregate (Wet) = ", volume_coarse_aggregate(i,f)*1.02)
        print("Fine Aggregate (Wet) = ", mass_basis(i,j)*1.06)
        print("Surface Water for Coarse Aggregate = ", 2-c)
        print("Surface Water for Fine Aggregate = ", 6-e)
        print("Water to be added = ", water_content_calculation(h,i,j)-(volume_coarse_aggregate(i,f)*((2-c)/100))-(mass_basis(i,j)*((6-e)/100)))
        print("Estimated Batch Mass Caoncrete, Total = ", water_content_calculation(h,i,j)-(volume_coarse_aggregate(i,f)*((2-c)/100))-(mass_basis(i,j)*((6-e)/100))+cement_content()+(volume_coarse_aggregate(i,f)*1.02)+(mass_basis(i,j)*1.06))
        print("----------------------------------------------------------------------------------------------------")
        print("Laboratory Trial Batch")
        print("Water Added = 2.7 Kg")
        print("Cement = ",cement_content()*0.02)
        print("Coarse Aggregate (Wet)", (volume_coarse_aggregate(i,f)*1.02)*0.02)
        print("Fine Aggregate (Wet)", (mass_basis(i,j)*1.06)*0.02)
        print("The estimated laboratory concrete, Total = ", (2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))
        print("----------------------------------------------------------------------------------------------------")
        if j == "non air entrained":
            print("Yield of Trial Batch Concrete = ", ((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))
        else:
            print("Yield of Trial Batch Concrete = ", ((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))
        print("----------------------------------------------------------------------------------------------------")
        print("Mixing Water Content = ", 2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))
        print("----------------------------------------------------------------------------------------------------")
        if j == "non air entrained":
            print("Final Water Content = ", (2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)
        else:
            print("Final Water Content = ", (2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)
        print("----------------------------------------------------------------------------------------------------")
        if j == "non air entrained":
            print("Final Cement Content = ", ((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j)))
        else:
            print("Final Cement Content = ", ((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j)))
        print("----------------------------------------------------------------------------------------------------")
        if j=="non air entrained":
            print("Final Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20)))
            print("SSD Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))*1.005)
            print("Final Fine Aggregate (Dry) = ", (table4_1[i]-20)-(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)+(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j)))+(((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))*1.005)))
        else:
            print("Final Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20)))
            print("SSD Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))*1.005)
            print("Final Fine Aggregate (Dry) = ", (table4_1[i]-20)-(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)+(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j)))+(((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))*1.005)))
        print("-----------------------------------------------------------------------------------------------------")
        if j == "non air entrained":
            print("Final Water Content = ", (2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)
            print("Final Cement Content = ", ((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j)))
            print("Final Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20)))
            print("SSD Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))*1.005)
            print("Final Fine Aggregate (Dry) = ", (table4_1[i]-20)-(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)+(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j)))+(((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))*1.005)))
            print("Ratio = ", 1," : ",((table4_1[i]-20)-(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)+(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j)))+(((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))*1.005)))/(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j))), " : ", (((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20)))/(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j)))," : ",((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_1[i]-20))+8)/(water_cement_ratio(k,j))) )
        else:
            print("Final Water Content = ", (2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)
            print("Final Cement Content = ", ((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j)))
            print("Final Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20)))
            print("SSD Coarse Aggregate (Dry) = ", ((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))*1.005)
            print("Final Fine Aggregate (Dry) = ", (table4_1[i]-20)-(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)+(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j)))+(((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))*1.005)))
            print("Ratio = ", 1," : ",((table4_2[i]-20)-(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)+(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j)))+(((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))*1.005)))/(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j))), " : ", (((volume_coarse_aggregate(i,f)*1.02)*0.02)/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20)))/(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j)))," : ",((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(((2.7+(((volume_coarse_aggregate(i,f)*1.02)*0.02)*((2-c)/(100)))+(((mass_basis(i,j)*1.06)*0.02)*((6-e)/(100))))/(((2.7)+(cement_content()*0.02)+((volume_coarse_aggregate(i,f)*1.02)*0.02)+((mass_basis(i,j)*1.06)*0.02))/(table4_2[i]-20))+8)/(water_cement_ratio(k,j))) )
        return "  ~~~~~~~~~  Code Executed Successfully (Design By Rupesh Sir) ~~~~~~~~~"
    a = float(input("Enter Specific Gravity of the Cement: "))
    b = float(input("Enter Specific Gravity of the coarse Aggregate: "))
    c = float(input("Enter Absorption of the Coarse Aggregate: "))
    d = float(input("Enter Specific Gravity of the Fine Aggregate: "))
    e = float(input("Enter Absorption of the Fine Aggregate: "))
    f = float(input("Enter Fineness Module of Fine Aggregate: "))
    g = float(input("Enter Coarse Aggregate dry-rodded mass in (Kg/m^3): "))
    h = float(input("Enter Slump Required in (mm): "))
    i = float(input("Enter the Nominal Size of Aggregate in (mm): "))
    j = input("Enter the Exposure: ")
    if j == "air entrained":
        m = input("Enter level of exposure: ")
    k = float(input("Enter the compressive strength in (Mpa): "))
    print(step_8(i,j))
