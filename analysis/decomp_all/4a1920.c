
void __fastcall FUN__text__004a1920(undefined4 param_1)

{
  undefined2 uVar1;
  undefined4 *puVar2;
  int iVar3;
  uint uVar4;
  undefined2 auStackY_1012c [32712];
  undefined4 local_188 [16];
  char local_148;
  int local_144;
  undefined1 local_140 [16];
  short local_130;
  undefined2 auStack_12c [100];
  undefined2 local_64;
  undefined2 local_60;
  uint local_5c;
  short asStack_58 [2];
  undefined4 uStack_54;
  undefined2 auStack_4e [31];
  uint local_10;
  uint local_c;
  undefined4 local_8;
  
  puVar2 = local_188;
  for (iVar3 = 0x61; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  local_8 = param_1;
  local_10 = CONCAT22(local_10._2_2_,1);
  local_5c = local_5c & 0xffff0000;
  local_60 = 0;
  local_c = local_c & 0xffff0000;
  while ((local_c & 0xffff) < 5) {
    puVar2 = (undefined4 *)FUN__text__004a95f0(local_140,local_c & 0xffff);
    uVar4 = local_c & 0xffff;
    *(undefined4 *)(asStack_58 + uVar4 * 7) = *puVar2;
    *(undefined4 *)((int)&uStack_54 + uVar4 * 0xe) = puVar2[1];
    *(undefined4 *)(&stack0xffffffb0 + uVar4 * 0xe) = puVar2[2];
    auStack_4e[uVar4 * 7 + 1] = *(undefined2 *)(puVar2 + 3);
    local_144 = (int)asStack_58[(local_c & 0xffff) * 7];
    if (local_144 == 2) {
      local_10 = local_10 & 0xffff0000;
      local_60 = auStack_4e[(local_c & 0xffff) * 7];
      uVar1 = FUN__text__004aa2a0(local_60);
      local_5c = CONCAT22(local_5c._2_2_,uVar1);
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  if ((local_10 & 0xffff) == 0) {
    if (*(short *)(&DAT_007a566c + (local_5c & 0xffff) * 0x10) < 1) {
      FUN__text__004aa0e0(local_60);
    }
    else {
      (&DAT_007a5668)[(local_5c & 0xffff) * 0x10] = 1;
      *(undefined2 *)(&DAT_007a566e + (local_5c & 0xffff) * 0x10) = 0;
    }
  }
  local_64 = 0;
  local_130 = 0;
  local_c = local_c & 0xffff0000;
  while ((int)(local_c & 0xffff) < (int)DAT_007a5b62) {
    *(short *)(&DAT_007a5670 + (local_c & 0xffff) * 0x10) =
         *(short *)(&DAT_007a5670 + (local_c & 0xffff) * 0x10) + 1;
    local_148 = (&DAT_007a5668)[(local_c & 0xffff) * 0x10];
    if (local_148 == '\0') {
      *(undefined2 *)(&DAT_007a566e + (local_c & 0xffff) * 0x10) = 0;
    }
    else if ((local_148 == '\x01') &&
            (*(short *)(&DAT_007a566e + (local_c & 0xffff) * 0x10) =
                  *(short *)(&DAT_007a566e + (local_c & 0xffff) * 0x10) + 1,
            *(short *)(&DAT_007a566c + (local_c & 0xffff) * 0x10) <=
            *(short *)(&DAT_007a566e + (local_c & 0xffff) * 0x10))) {
      (&DAT_007a5668)[(local_c & 0xffff) * 0x10] = 0;
    }
    if ((-1 < *(short *)(&DAT_007a566a + (local_c & 0xffff) * 0x10)) &&
       (*(short *)(&DAT_007a566a + (local_c & 0xffff) * 0x10) <=
        *(short *)(&DAT_007a5670 + (local_c & 0xffff) * 0x10))) {
      auStack_12c[local_130] = *(undefined2 *)(&DAT_007a5662 + (local_c & 0xffff) * 0x10);
      local_130 = local_130 + 1;
    }
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_c = local_c & 0xffff0000;
  while ((int)(local_c & 0xffff) < (int)local_130) {
    FUN__text__004aa0e0(auStack_12c[local_c & 0xffff]);
    local_c = CONCAT22(local_c._2_2_,(short)local_c + 1);
  }
  local_8 = 0x4a1c67;
  FUN__text__0056ce80();
  return;
}

