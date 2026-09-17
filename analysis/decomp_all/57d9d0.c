
void FUN_0057d9d0(int param_1)

{
  code *pcVar1;
  int iVar2;
  size_t sVar3;
  undefined1 *puVar4;
  undefined4 uVar5;
  undefined1 local_1b4 [160];
  char local_114 [260];
  char *local_10;
  uint local_c;
  undefined1 local_8 [4];
  
  for (local_c = 0; (local_c < 0x12 && (param_1 != *(int *)(&DAT_007644f8 + local_c * 8)));
      local_c = local_c + 1) {
  }
  if (param_1 == *(int *)(&DAT_007644f8 + local_c * 8)) {
    if ((param_1 != 0xfc) &&
       (iVar2 = FUN_00573780(1,0,0,0,(&PTR_s_R6002___floating_point_not_loade_007644fc)[local_c * 2]
                            ), iVar2 == 1)) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    if ((DAT_0080a468 == 1) || ((DAT_0080a468 == 0 && (DAT_007619fc == 1)))) {
      uVar5 = 0;
      puVar4 = local_8;
      sVar3 = _strlen((&PTR_s_R6002___floating_point_not_loade_007644fc)[local_c * 2]);
      uVar5 = (*API_KERNEL32_DLL_GetStdHandle)
                        (0xfffffff4,(&PTR_s_R6002___floating_point_not_loade_007644fc)[local_c * 2],
                         sVar3,puVar4,uVar5);
      (*DAT_005922bc)(uVar5);
    }
    else if (param_1 != 0xfc) {
      iVar2 = (*API_KERNEL32_DLL_GetModuleFileNameA)(0,local_114,0x104);
      if (iVar2 == 0) {
        FUN_0056cd90(local_114,"<program name unknown>");
      }
      local_10 = local_114;
      sVar3 = _strlen(local_10);
      if (0x3c < sVar3 + 1) {
        sVar3 = _strlen(local_114);
        local_10 = local_10 + (sVar3 - 0x3b);
        _strncpy(local_10,"...",3);
      }
      FUN_0056cd90(local_1b4,"Runtime Error!\n\nProgram: ");
      FUN_0056cda0(local_1b4,local_10);
      FUN_0056cda0(local_1b4,&DAT_005f9f3c);
      FUN_0056cda0(local_1b4,(&PTR_s_R6002___floating_point_not_loade_007644fc)[local_c * 2]);
      FUN_00584390(local_1b4,"Microsoft Visual C++ Runtime Library",0x12010);
    }
  }
  return;
}

