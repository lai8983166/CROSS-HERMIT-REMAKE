
void FUN__text__00450570(undefined4 param_1,int *param_2,undefined4 param_3,undefined4 param_4)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_68 [16];
  int local_28;
  int local_24;
  int local_20;
  int local_1c;
  int local_18;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB__text__0058f6cb;
  local_10 = ExceptionList;
  puVar3 = local_68;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  ExceptionList = &local_10;
  local_24 = FUN__text__00428a40(0xba20);
  local_8 = 0;
  if (local_24 == 0) {
    local_28 = 0;
  }
  else {
    local_28 = FUN__text__00412e30();
  }
  local_20 = local_28;
  local_8 = 0xffffffff;
  local_18 = local_28;
  if (local_28 != 0) {
    uVar1 = FUN__text__004500b0("data\\");
    local_1c = FUN__text__004135d0(uVar1);
    if (local_1c != 0) {
      (*DAT_005923d8)(param_1,&DAT_00598718,"Cross Hermit",0x10);
      FUN__text__0056ce80();
    }
    local_1c = FUN__text__00413630();
    if (local_1c != 0) {
      (*DAT_005923d8)(param_1,&DAT_005986e0,"Cross Hermit",0x10);
      FUN__text__0056ce80();
    }
    local_1c = FUN__text__00413450(param_1,0,1,param_3,param_4);
    if (local_1c == 0) {
      local_1c = FUN__text__00413560();
      if (local_1c == 0) {
        *param_2 = local_18;
        goto LAB__text__0045070e;
      }
      FUN__text__00413360();
      (*DAT_005923d8)(param_1,&DAT_005986ac,"Cross Hermit",0x10);
      FUN__text__0056ce80();
    }
    else {
      (*DAT_005923d8)(param_1,&DAT_005986c8,"Cross Hermit",0x10);
      FUN__text__0056ce80();
    }
    if (local_18 != 0) {
      *param_2 = local_18;
      FUN__text__00450730(param_2);
    }
  }
LAB__text__0045070e:
  ExceptionList = local_10;
  local_8 = 0x450725;
  FUN__text__0056ce80();
  return;
}

