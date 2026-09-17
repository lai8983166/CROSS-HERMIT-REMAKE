
void FUN__text__004b7e90(undefined2 param_1,short param_2,short param_3,undefined4 param_4,
                        undefined2 param_5,undefined2 param_6,undefined2 param_7,undefined4 param_8,
                        uint param_9,short param_10)

{
  int iVar1;
  int iVar2;
  undefined2 extraout_var;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined *local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__004d1ba0(param_4,0,(int)param_3);
  if (param_10 != 0) {
    FUN__text__004b7120(param_1,iVar2,1,CONCAT22(extraout_var,param_6),param_7);
  }
  if (param_2 != -1) {
    iVar1 = (uint)*(ushort *)(&DAT_0061c288 + param_2 * 8) * 0x10;
    local_c = &DAT_0061bae0 + iVar1;
    FUN__text__004d2dd0(0xd,param_5,*(undefined2 *)(&DAT_0061bae2 + iVar1),
                        (int)*(short *)(&DAT_0061c28c + param_2 * 8),
                        (int)*(short *)(&DAT_0061c28e + param_2 * 8),
                        *(undefined2 *)(&DAT_0061bae4 + iVar1),
                        (uint)*(ushort *)(&DAT_0061bae6 + iVar1) +
                        (param_9 & 0xffff) * (uint)*(ushort *)(&DAT_0061baea + iVar1),
                        *(undefined2 *)(&DAT_0061bae8 + iVar1),
                        *(undefined2 *)(&DAT_0061baea + iVar1),
                        (int)(((ulonglong)(uint)(iVar2 * 100) / (ulonglong)(uint)(int)param_3) %
                             0x65),100);
  }
  local_8 = 0x4b7fb9;
  FUN__text__0056ce80();
  return;
}

