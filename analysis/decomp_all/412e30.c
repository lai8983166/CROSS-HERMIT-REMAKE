
void FUN__text__00412e30(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_5c [16];
  int local_1c;
  int local_18;
  int local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058ecfe;
  local_10 = ExceptionList;
  puVar3 = local_5c;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  FUN__text__00409900();
  local_8 = 0;
  FUN__text__00417530();
  local_8._0_1_ = 1;
  FUN__text__0041ee30();
  local_8._0_1_ = 2;
  FUN__text__0041ead0();
  local_8._0_1_ = 3;
  FUN__text__0040d7e0();
  local_8._0_1_ = 4;
  FUN__text__00410c20();
  local_8._0_1_ = 5;
  FUN__text__0040be70();
  local_8._0_1_ = 6;
  FUN__text__0041d0d0();
  local_8._0_1_ = 7;
  FUN__text__00417c40();
  local_8 = CONCAT31(local_8._1_3_,8);
  *(undefined4 *)(local_14 + 0xb1f8) = 1;
  *(undefined4 *)(local_14 + 0xb1fc) = 0x40;
  *(undefined4 *)(local_14 + 0xb200) = 0;
  *(undefined4 *)(local_14 + 0xb270) = 0;
  *(undefined4 *)(local_14 + 0xb26c) = 0;
  for (local_18 = 0; local_18 != 2; local_18 = local_18 + 1) {
    *(undefined4 *)(local_14 + 0x1090 + local_18 * 4) = 0;
  }
  _memset((void *)(local_14 + 0xb234),0,0x34);
  *(undefined4 *)(local_14 + 0xb278) = 0;
  *(undefined4 *)(local_14 + 0xb27c) = 0;
  *(undefined4 *)(local_14 + 0xb284) = 0;
  *(undefined4 *)(local_14 + 0xb280) = 0;
  *(undefined4 *)(local_14 + 0xb204) = 0;
  (*API_USER32_DLL_GetDC)(0);
  uVar1 = FUN__text__0056ce80();
  *(undefined4 *)(local_14 + 0xb208) = uVar1;
  *(undefined4 *)(local_14 + 0xb20c) = 0;
  *(undefined4 *)(local_14 + 0xb210) = 0;
  _memset((void *)(local_14 + 0xb214),0,0x10);
  *(undefined4 *)(local_14 + 0xb310) = 0;
  *(undefined1 *)(local_14 + 0xb274) = 0;
  *(undefined1 *)(local_14 + 0xb275) = 0;
  *(undefined1 *)(local_14 + 0xb276) = 0;
  *(undefined1 *)(local_14 + 0xb277) = 0;
  *(undefined4 *)(local_14 + 0xb180) = 1;
  *(undefined4 *)(local_14 + 0xb190) = 0;
  *(undefined4 *)(local_14 + 0xb194) = 0;
  *(undefined4 *)(local_14 + 0xb198) = 0;
  *(undefined4 *)(local_14 + 0xb19c) = 0;
  FUN__text__0040b590();
  FUN__text__00415a90();
  *(undefined2 *)(local_14 + 0xb288) = 0;
  *(undefined2 *)(local_14 + 0xb28a) = 1;
  *(undefined2 *)(local_14 + 0xb28c) = 0;
  *(undefined2 *)(local_14 + 0xb28e) = 1;
  FUN__text__00414f90(0);
  *(undefined4 *)(local_14 + 0xb188) = 1;
  *(undefined4 *)(local_14 + 0xb18c) = 0;
  (*API_KERNEL32_DLL_QueryPerformanceFrequency)(local_14 + 0xb188);
  local_1c = FUN__text__0056ce80();
  if (local_1c == 0) {
    *(undefined4 *)(local_14 + 0xb188) = 0;
    *(undefined4 *)(local_14 + 0xb18c) = 0;
  }
  FUN__text__00415370();
  local_8 = 0xffffffff;
  ExceptionList = local_10;
  local_10 = (void *)0x41313e;
  FUN__text__0056ce80();
  return;
}

