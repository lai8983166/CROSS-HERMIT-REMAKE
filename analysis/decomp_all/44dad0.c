
void FUN__text__0044dad0(void)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 local_5c [16];
  int local_1c;
  undefined4 local_18;
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_5c;
  for (iVar2 = 0x16; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_14 = 0;
  uVar1 = FUN__text__0044d9d0(0x138,299,&PTR_DAT_006067a8,1);
  *(undefined4 *)(local_8 + 0x38) = uVar1;
  uVar1 = FUN__text__0044d9d0(0x138,299,&DAT_006067b8,10);
  *(undefined4 *)(local_8 + 0x3c) = uVar1;
  uVar1 = FUN__text__0044d9d0(0x138,299,&DAT_00606808,10);
  *(undefined4 *)(local_8 + 0x40) = uVar1;
  uVar1 = FUN__text__0044d9d0(0x138,299,&DAT_00606858,10);
  *(undefined4 *)(local_8 + 0x44) = uVar1;
  if ((((*(int *)(local_8 + 0x38) == -1) && (*(int *)(local_8 + 0x3c) == -1)) &&
      (*(int *)(local_8 + 0x40) == -1)) && (*(int *)(local_8 + 0x44) == -1)) {
    local_1c = 0;
  }
  else {
    local_1c = 1;
  }
  local_10 = local_1c;
  if ((local_1c != 0) && ((*(uint *)(DAT_007a49fc + 0x199c) & 1) != 0)) {
    if (*(int *)(local_8 + 0x38) == -1) {
      if (*(int *)(local_8 + 0x3c) == -1) {
        if (*(int *)(local_8 + 0x40) == -1) {
          if ((*(int *)(local_8 + 0x44) != -1) &&
             (*(int *)(local_8 + 0x50) != *(int *)(local_8 + 0x44))) {
            *(undefined4 *)(local_8 + 0x50) = *(undefined4 *)(local_8 + 0x44);
            local_18 = FUN__text__004e2ec0(*(undefined4 *)(local_8 + 0x50));
            FUN__text__0041da10(local_18);
            FUN__text__0041da80(local_18);
            uVar4 = 0;
            uVar1 = FUN__text__004501d0("data\\sound\\Voice\\v006\\v006_043_01.mp3");
            FUN__text__0041e190(uVar1,uVar4);
          }
        }
        else if (*(int *)(local_8 + 0x4c) != *(int *)(local_8 + 0x40)) {
          *(undefined4 *)(local_8 + 0x4c) = *(undefined4 *)(local_8 + 0x40);
          local_18 = FUN__text__004e2ef0(*(undefined4 *)(local_8 + 0x4c));
          FUN__text__0040d6c0(local_18);
          FUN__text__0040d390(0,0xb,0,0);
        }
      }
      else if (*(int *)(local_8 + 0x48) != *(int *)(local_8 + 0x3c)) {
        *(undefined4 *)(local_8 + 0x48) = *(undefined4 *)(local_8 + 0x3c);
        local_18 = FUN__text__004e2ec0(*(undefined4 *)(local_8 + 0x48));
        FUN__text__0041da10(local_18);
        FUN__text__0041da80(local_18);
      }
    }
    else {
      FUN__text__004db2b0(5);
      FUN__text__0044d5b0();
      local_14 = 1;
    }
  }
  if ((*(uint *)(DAT_007a49fc + 0x198c) & 1) == 0) {
    for (local_c = 0; local_c != 4; local_c = local_c + 1) {
      *(undefined4 *)(local_8 + 0x38 + local_c * 4) = 0xffffffff;
    }
  }
  local_8 = 0x44dd8c;
  FUN__text__0056ce80();
  return;
}

