
void FUN__text__004c2d80(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined1 *local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 4) >> 0x1c,
                              *(uint *)(param_2 + 4) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9250) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 8) >> 0x1c,
                              *(uint *)(local_c + 8) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9254) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0xc) >> 0x1c,
                              *(uint *)(local_c + 0xc) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9258) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x10) >> 0x1c,
                              *(uint *)(local_c + 0x10) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x925c) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x14) >> 0x1c,
                              *(uint *)(local_c + 0x14) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9260) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x18) >> 0x1c,
                              *(uint *)(local_c + 0x18) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9264) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x1c) >> 0x1c,
                              *(uint *)(local_c + 0x1c) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9268) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x20) >> 0x1c,
                              *(uint *)(local_c + 0x20) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x926c) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x24) >> 0x1c,
                              *(uint *)(local_c + 0x24) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9270) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x28) >> 0x1c,
                              *(uint *)(local_c + 0x28) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9274) = uVar1;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(local_c + 0x2c) >> 0x1c,
                              *(uint *)(local_c + 0x2c) & 0xfffffff);
  *(undefined4 *)(local_8 + 0x9278) = uVar1;
  local_10 = (undefined1 *)(local_8 + 0x228 + *(int *)(local_8 + 0x9250) * 0x1a);
  *local_10 = 1;
  FUN__text__004cb9f0(3);
  FUN__text__004cb850(*(undefined4 *)(local_8 + 0x9254),*(undefined4 *)(local_8 + 0x9258));
  FUN__text__004cb970(*(undefined4 *)(local_8 + 0x925c));
  FUN__text__004cb9b0(*(undefined4 *)(local_8 + 0x9260));
  FUN__text__004cb910(*(undefined4 *)(local_8 + 0x9264),*(undefined4 *)(local_8 + 0x9268),
                      *(undefined4 *)(local_8 + 0x926c),*(undefined4 *)(local_8 + 0x9270));
  FUN__text__004cba20(*(undefined4 *)(local_8 + 0x9274),*(undefined4 *)(local_8 + 0x9278));
  local_8 = 0x4c3077;
  FUN__text__0056ce80();
  return;
}

