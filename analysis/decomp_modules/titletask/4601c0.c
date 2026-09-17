
void __fastcall FUN__text__004601c0(undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_58 [16];
  int local_18;
  undefined4 *local_14;
  void *local_10;
  undefined1 *puStack_c;
  uint local_8;
  
  puStack_c = &LAB__text__0058fb35;
  local_10 = ExceptionList;
  puVar2 = local_58;
  for (iVar1 = 0x12; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  ExceptionList = &local_10;
  *param_1 = &PTR_DAT_0059b0e4;
  local_8 = 1;
  local_14 = param_1;
  FUN__text__0041d280();
  FUN__text__0040d610();
  FUN__text__0041f4e0(0x5a);
  FUN__text__0041f480();
  for (local_18 = 1; local_18 != 0x14; local_18 = local_18 + 1) {
    FUN__text__0040d120(local_18);
  }
  DAT_007a49d4 = DAT_007a49d4 + 1;
  local_8 = local_8 & 0xffffff00;
  FUN__text__00407710();
  local_8 = 0xffffffff;
  FUN__text__00439f80();
  ExceptionList = local_10;
  local_8 = 0x4602b9;
  FUN__text__0056ce80();
  return;
}

