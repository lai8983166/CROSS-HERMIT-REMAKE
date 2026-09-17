
void __fastcall FUN__text__00506290(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  puStack_c = &LAB__text__00590d09;
  local_10 = ExceptionList;
  puVar2 = local_58;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_005caa48;
  local_8 = 0;
  local_14 = param_1;
  FUN__text__0041d280();
  FUN__text__0040d610();
  FUN__text__0041f4e0(10);
  for (local_18 = 0; local_18 != 10; local_18 = local_18 + 1) {
    FUN__text__00464d30();
  }
  local_8 = 0xffffffff;
  FUN__text__00504e10();
  ExceptionList = local_10;
  local_8 = 0x50635c;
  FUN__text__0056ce80();
  return;
}

