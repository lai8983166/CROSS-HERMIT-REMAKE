
void FUN__text__0042f2d0(undefined4 param_1,int param_2)

{
  undefined4 uVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  undefined4 local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = param_2;
  uVar1 = FUN__text__004c1eb0(param_1,*(uint *)(param_2 + 8) >> 0x1c,
                              *(uint *)(param_2 + 8) & 0xfffffff);
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
  local_10 = FUN__text__004997d0(*(undefined4 *)(local_8 + 0x9254),*(undefined4 *)(local_8 + 0x9258)
                                 ,*(undefined4 *)(local_8 + 0x925c),
                                 *(undefined4 *)(local_8 + 0x9260),*(undefined4 *)(local_8 + 0x9264)
                                );
  FUN__text__004c1f40(param_1,*(uint *)(local_c + 4) >> 0x1c,*(uint *)(local_c + 4) & 0xfffffff,
                      local_10);
  local_8 = 0x42f451;
  FUN__text__0056ce80();
  return;
}

