
void FUN__text__0044fbb0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f5b7;
  local_10 = ExceptionList;
  puVar3 = local_54;
  for (iVar2 = 0x11; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00439d10();
  local_8 = 0;
  FUN__text__00424670();
  local_8._0_1_ = 1;
  FUN__text__00429310();
  local_8._0_1_ = 2;
  FUN__text__00423480();
  local_8._0_1_ = 3;
  FUN__text__00421540();
  local_8._0_1_ = 4;
  FUN__text__00425780();
  local_8._0_1_ = 5;
  FUN__text__00428b90();
  local_8 = CONCAT31(local_8._1_3_,6);
  *local_14 = &PTR_DAT_005986a0;
  local_14[0x234] = 0;
  _memset(local_14 + 0x235,0,0xc);
  _memset(local_14 + 0x27b,0,0x104);
  _memset(local_14 + 0x2fd,0,0x104);
  _memset(local_14 + 0x33e,0,0x104);
  _memset(local_14 + 0x3c0,0,0x104);
  _memset(local_14 + 0x401,0,0x104);
  uVar1 = FUN__text__00429540();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 0x27b,uVar1);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 700,local_14 + 0x27b);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 0x2fd,local_14 + 0x27b);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 0x33e,local_14 + 0x27b);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 0x37f,local_14 + 0x27b);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 0x3c0,local_14 + 0x27b);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcpyA)(local_14 + 0x401,local_14 + 0x27b);
  FUN__text__0056ce80();
  (*API_KERNEL32_DLL_lstrcatA)(local_14 + 0x401,"SaveData\\");
  FUN__text__0056ce80();
  local_14[0x442] = 0;
  local_14[0x238] = 0;
  local_14[0x239] = 0;
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  local_54[3] = 0x44fe50;
  FUN__text__0056ce80();
  return;
}

