
bool FUN_00573b10(int param_1,undefined *param_2,undefined *param_3,char *param_4,char *param_5)

{
  int iVar1;
  size_t sVar2;
  char *local_113c;
  char *local_1138;
  char *local_1134;
  undefined *local_1130;
  char *local_112c;
  undefined *local_1128;
  undefined *local_1124;
  char *local_1114;
  undefined1 local_1110 [4036];
  char acStackY_14c [60];
  int local_110;
  char local_10c [188];
  undefined4 uStackY_50;
  undefined1 *puStackY_4c;
  undefined4 uStackY_48;
  char *pcStackY_44;
  undefined *puStackY_40;
  char *pcStackY_3c;
  char *pcStackY_38;
  char *pcStackY_34;
  char *pcStackY_30;
  undefined *puStackY_2c;
  char *pcStackY_28;
  undefined *puStackY_24;
  undefined *puStackY_20;
  char *local_8;
  
  FUN_0056e230();
  if ((param_5 == (char *)0x0) && (iVar1 = FUN_00573780(), iVar1 == 1)) {
    FUN_00573670();
  }
  iVar1 = (*API_KERNEL32_DLL_GetModuleFileNameA)();
  if (iVar1 == 0) {
    FUN_0056cd90();
  }
  local_8 = local_10c;
  sVar2 = _strlen(local_8);
  if (0x40 < sVar2) {
    sVar2 = _strlen(local_8);
    local_8 = acStackY_14c + sVar2;
    puStackY_20 = (undefined *)0x573bba;
    _strncpy(local_8,"...",3);
  }
  local_1114 = param_4;
  if ((param_4 != (char *)0x0) && (sVar2 = _strlen(param_4), 0x40 < sVar2)) {
    sVar2 = _strlen(param_4);
    local_1114 = param_4 + (sVar2 - 0x40);
    puStackY_20 = (undefined *)0x573c15;
    _strncpy(local_1114,"...",3);
  }
  if (*param_5 == '\0') {
    local_1124 = &DAT_005953ac;
  }
  else {
    local_1124 = &DAT_005f9f3c;
  }
  if (param_3 == (undefined *)0x0) {
    local_1128 = &DAT_005953ac;
    local_112c = "";
    puStackY_24 = local_1128;
  }
  else {
    local_112c = "\nLine: ";
    puStackY_24 = param_3;
  }
  if (param_2 == (undefined *)0x0) {
    local_1130 = &DAT_005953ac;
    local_1134 = "";
    puStackY_2c = local_1130;
  }
  else {
    local_1134 = "\nFile: ";
    puStackY_2c = param_2;
  }
  if (local_1114 == (char *)0x0) {
    local_1138 = "";
    local_113c = "";
    pcStackY_34 = local_1138;
  }
  else {
    local_113c = "\nModule: ";
    pcStackY_34 = local_1114;
  }
  puStackY_20 = local_1124;
  pcStackY_28 = local_112c;
  pcStackY_30 = local_1134;
  pcStackY_38 = local_113c;
  pcStackY_3c = local_8;
  puStackY_40 = (&PTR_s_Warning_00761b8c)[param_1];
  pcStackY_44 = 
  "Debug %s!\n\nProgram: %s%s%s%s%s%s%s%s%s%s%s\n\n(Press Retry to debug the application)";
  uStackY_48 = 0x1000;
  puStackY_4c = local_1110;
  uStackY_50 = 0x573db2;
  iVar1 = FUN_005715b0();
  if (iVar1 < 0) {
    FUN_0056cd90();
  }
  puStackY_20 = (undefined *)0x573de3;
  local_110 = FUN_00584390();
  if (local_110 == 3) {
    FUN_005840d0();
                    /* WARNING: Subroutine does not return */
    __exit(3);
  }
  return local_110 == 4;
}

